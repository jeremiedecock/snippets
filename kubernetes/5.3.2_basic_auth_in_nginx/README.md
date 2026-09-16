# Password-protecting the app with HTTP Basic auth (htpasswd), in nginx itself

This example is [`5.3.1_basic_auth_in_envoy`](../5.3.1_basic_auth_in_envoy/)
with the password check moved **one hop further in**: same URL, same
credentials, same htpasswd file — but it is the **nginx Pod** that answers
`401`, not the Gateway.

Read 5.3.1 first. It is where HTTP Basic auth itself is explained — the
`401`/`WWW-Authenticate` exchange, why base64 is not a security measure, why
there is no logout — and none of that is repeated here. This directory is
about *where the check belongs*, which is a deployment question rather than a
protocol one.

Like 5.3.1, it **continues [`5.2_lets_encrypt`](../5.2_lets_encrypt/)**: the
Gateway, the certificate, the routes and the namespace are the ones already
running there. Run 5.2 first and stop before its *Remove the demo* section.

The two examples are **mutually exclusive on a running cluster**. If 5.3.1 is
still applied, delete its SecurityPolicy before starting (there is a command
for it in *Prerequisites*) — two independent gates on one URL work, but the
demo stops demonstrating anything.

## What changes compared to `5.3.1_basic_auth_in_envoy`

The htpasswd file is the same, the Secret is the same, the namespace is the
same, the certificate is the same. What moves is the enforcement point:

| | `5.3.1` (Envoy) | `5.3.2` (here, nginx) |
| --- | --- | --- |
| Who answers `401` | the Envoy proxy | the nginx Pod |
| Manifests applied | one `SecurityPolicy` | a `ConfigMap` + a patched `Deployment` |
| The app image | untouched, not even restarted | untouched, but **redeployed** with a config |
| Portable across Gateway API implementations | **no** (Envoy Gateway extension) | **yes** — plain Kubernetes objects |
| Hash algorithms | **SHA-1 only** (`htpasswd -s`) | bcrypt, SHA-256/512, MD5-apr1, SHA-1 |
| Granularity | the whole HTTPRoute | per `location`, with `auth_basic off` to opt out |
| The realm | imposed (built from the request URI) | any string you choose |
| Unauthenticated traffic reaching the Pod | **none** — rejected at the Gateway | **all of it** — nginx parses it to refuse it |
| Who sees the failed logins | the Envoy Gateway proxy logs | `kubectl logs` on the app itself |
| Changing the password | Secret → proxy reconfigured | Secret → nginx re-reads it, no restart |
| Changing the rules | edit the SecurityPolicy | edit the ConfigMap, **restart the Pod** |

Three of those rows are the reason this example exists. Taken in order of how
much they matter:

### 1. The hash is no longer the worst one available

Half of 5.3.1's README is a warning about `htpasswd -s`: Envoy reads *only*
unsalted SHA-1, so the example is forced to use the weakest entry in the
table, and to compensate with "use long random passwords, treat the file as
compromised if it leaks".

nginx has no such limit. Its
[auth_basic_user_file](https://nginx.org/en/docs/http/ngx_http_auth_basic_module.html#auth_basic_user_file)
accepts:

| `htpasswd` flag | Prefix | Supported by nginx | By Envoy (5.3.1) |
| --- | --- | --- | --- |
| `-B` bcrypt | `$2y$` | yes, through the C library's `crypt()` | no |
| `-2` / `-5` SHA-256/512 crypt | `$5$` / `$6$` | yes, through `crypt()` | no |
| *(none)* / `-m` MD5 apr1 | `$apr1$` | yes, implemented by nginx itself | no |
| `-s` SHA-1 | `{SHA}` | yes, and documented as *should not be used* | **the only one** |

**Use `-B`.** bcrypt is salted and deliberately slow, which is the whole point
of a password hash; the offline-cracking paragraph of 5.3.1 simply stops
applying. *How* slow is a separate question, and one where this example
deliberately stays modest — see *The cost, and why the default stays* below.

One caveat, because nginx's documentation is worth reading literally: what it
promises is `$apr1$`, `{SHA}`, `{SSHA}` — which it implements itself — and
"passwords encrypted with the `crypt()` function", which it delegates to the C
library. bcrypt is in that last group, so it works because *musl* (the Alpine
images used here) and *libxcrypt* (today's Debian and Fedora) implement it,
not because nginx does. On these images it works; on an exotic base image,
`$apr1$` is the format that cannot let you down.

### 2. The manifests are portable

Nothing in this directory names a Gateway API implementation. Put Traefik,
Istio, Cilium or an old-style Ingress in front of it and the password still
works, because the thing asking for it is the app's own web server. 5.3.1's
`SecurityPolicy` has to be rewritten as a Traefik `Middleware`, an Istio
`AuthorizationPolicy` or an ingress-nginx annotation for each move.

The same reasoning removes a hazard 5.3.1 has to design around. There, the
policy had to target the HTTPRoute rather than the Gateway, or the ACME
HTTP-01 challenge would have been answered with a `401` and **certificate
renewal would have failed silently two months later**. Here the question does
not arise: cert-manager serves the challenge from its own solver Pod, which is
not this nginx, and nothing this directory applies can touch it.

### 3. The app now sees unauthenticated traffic

This is the argument for the other side, and it is the real one.

```
5.3.1   internet --HTTPS--> Gateway (TLS + password) --HTTP--> Pod
                            401 stops here ^                   ^ only authenticated requests arrive

5.3.2   internet --HTTPS--> Gateway (TLS)            --HTTP--> Pod (password)
                                                               ^ every request arrives, including the refused ones
```

With the check at the Gateway, a request carrying no credentials is refused by
Envoy and the Pod never hears about it: nginx only ever parses requests that
already passed. Here, every scanner, every bot and every malformed request
reaches nginx, which has to read the request line, the headers and the URI
*before* it can decide to answer `401`. That pre-authentication attack surface
is what a gateway-level gate actually buys, and giving it up is the honest
cost of this example.

It is **not**, despite the intuition, about the password on the wire. Envoy's
basic auth filter validates the `Authorization` header and forwards the
request upstream unchanged, header included — so in 5.3.1 the credentials
already cross the Gateway → Pod hop in plain HTTP, exactly as they do here.
The difference is only that 5.3.1 *could* strip them, with a
`RequestHeaderModifier` filter on the HTTPRoute; TLS terminates at the Gateway
in both cases, and inside the cluster nothing is encrypted in either unless a
service mesh provides mTLS.

## The two manifests

`nginx-conf.yml` — a ConfigMap holding one nginx `server` block. Three
directives do the work:

```nginx
auth_basic           "Restricted area";
auth_basic_user_file /etc/nginx/secrets/.htpasswd;
```

and, in the health-check `location`:

```nginx
auth_basic off;
```

`deployment.yml` — 5.2's Deployment with the ConfigMap mounted over
`/etc/nginx/conf.d`, the Secret mounted at `/etc/nginx/secrets`, and a
`readinessProbe` on `/healthz`. The probe is there on purpose: the kubelet
requests it from the Pod's IP with no credentials, so if the `auth_basic off`
block is missing or misspelled, the Pod stays `0/1 Ready` and the rollout
hangs. It is the cheapest possible demonstration of why a gate on *everything*
is rarely what you want.

Both files are commented; the comments carry the details this README does not
repeat (why `0444` and not `0400`, why the ConfigMap key has to end in
`.conf`, why neither mount uses `subPath`).

## Prerequisites

**[`5.2_lets_encrypt`](../5.2_lets_encrypt/), deployed and still running** —
Gateway `PROGRAMMED=True`, certificate `READY=True`, both HTTPRoutes present:

```shell
kubectl get gateway,httproute,certificate -n snippet-letsencrypt-demo
```

Unlike 5.3.1, **any** Gateway API implementation will do — Envoy Gateway is
simply what 5.2 set up.

If you ran [`5.3.1_basic_auth_in_envoy`](../5.3.1_basic_auth_in_envoy/),
remove its policy, so that the `401` you get later is unambiguously nginx's:

```shell
kubectl delete securitypolicy my-basic-auth -n snippet-letsencrypt-demo --ignore-not-found
```

The site must then answer without a password:

```shell
curl -i https://my-app.example.com/
```

Use the domain you put in 5.2's manifests wherever `my-app.example.com`
appears below. As in 5.3.1, nothing in this directory contains a hostname —
`server_name _;` matches whatever the Gateway forwards — so there is no `sed`
to run.

And **`htpasswd`** (`apache2-utils` on Debian/Ubuntu, `httpd-tools` on
Fedora/RHEL, `apache2` in Homebrew). This time it is closer to a real
requirement: the `openssl` one-liner of 5.3.1 produces the SHA-1 format, and
the point here is to stop using it.

## Create the password file

Same file, better hash. `-c` creates it and **truncates an existing one**;
`-B` selects bcrypt; omitting `-b` makes `htpasswd` prompt instead of taking
the password from the command line, keeping it out of your shell history:

```shell
openssl rand -base64 24     # a password worth the name

htpasswd -c -B .htpasswd alice
htpasswd -B .htpasswd bob   # no -c, or you lose alice
```

Check what came out. This is 5.3.1's verification step with the expectation
inverted — there, `$2y$` was the failure:

```shell
cat .htpasswd
```

```
alice:$2y$05$nRwEHKsFZCJ1zGcJ0FNaFwEaDPjzQNlVLWtKGFY90m54skdVdIk9p
bob:$2y$05$3iHNzTpR8zDHmpq94GJg6GFl3ivqA5rTM9FZiOdww9IT3xhP1hzru
```

`$2y$` is bcrypt. `$apr1$` (MD5) would also work; `{SHA}` would work too and
would mean you copied the command from 5.3.1.

### The cost, and why the default stays

Raising bcrypt's cost is a flag away: each step doubles the work per attempt,
so `-C 12` is 128 times `htpasswd`'s default of 5 (the valid range is 4 to
17). For a password *database*, 10 to 12 is where current advice sits, and 5
looks indefensibly low.

Do not do it here, and the reason is worth a paragraph because it is the one
argument that does not generalise from "how to store passwords" to "how to
check them in a proxy". Two properties combine badly:

- **Basic auth re-authenticates every single request.** There is no session,
  no cookie, nothing to remember — that is the property 5.3.1 spent a section
  on. The hash is recomputed for every image, every stylesheet, every reload.
- **An nginx worker is a single-threaded event loop, and `crypt_r()` blocks
  it.** There is no thread pool for this: while a worker computes a bcrypt,
  every other connection assigned to that worker waits.

At `-C 5` the check costs a couple of milliseconds and disappears into the
noise. At `-C 12` it costs something like a quarter of a second, *per
request*, monopolising a worker for the duration. A handful of concurrent
requests carrying deliberately wrong credentials is then enough to saturate
every worker on the Pod — and the cost is paid **before** anyone knows the
password is wrong, so it is a denial of service available to unauthenticated
clients for free, from a laptop.

The same reasoning applies to `htpasswd -5 -r 100000` and, more so, to a
memory-hard hash such as yescrypt: the stronger the hash, the cheaper the
attack on the server that computes it once per request.

There is a symmetry with 5.3.1 worth noticing here. Envoy's SHA-1 is
contemptible against an attacker holding a copy of the file, and free to
compute — no request cost, no worker to block. bcrypt reverses both. Neither
directory gets to have it both ways, and a rate limit is what buys back the
difference: `limit_req` on the protected location bounds how many hashes a
client can make nginx compute, and is the thing to add *before* raising `-C`,
not after.

So the honest position is that a *high* cost belongs where authentication
happens **once** and issues a session — an OIDC proxy, a forward-auth
service, an application setting a cookie. Basic auth structurally cannot use
one, so it pairs a sound algorithm with a deliberately modest cost, and leans
on password *length* for the rest: a 24-byte random password is out of reach
of an offline attack whatever the cost factor, which is exactly what the
`openssl rand` above is for.

`.htpasswd` is listed in `.gitignore` here. Keep it that way.

## Put it in a Secret

Identical to 5.3.1 — the key must be exactly `.htpasswd`, because
`deployment.yml` mounts the Secret as a directory and the key becomes the file
name that `auth_basic_user_file` points at:

```shell
kubectl create secret generic basic-auth-users \
  --from-file=.htpasswd \
  -n snippet-letsencrypt-demo
```

If 5.3.1 already created it with the SHA-1 file, replace it rather than
failing on "already exists":

```shell
kubectl create secret generic basic-auth-users \
  --from-file=.htpasswd \
  -n snippet-letsencrypt-demo \
  --dry-run=client -o yaml | kubectl apply -f -
```

Read it back, and confirm the hashes survived:

```shell
kubectl get secret basic-auth-users -n snippet-letsencrypt-demo \
  -o jsonpath='{.data.\.htpasswd}' | base64 -d
```

## Apply

```shell
kubectl apply -f nginx-conf.yml -f deployment.yml -n snippet-letsencrypt-demo
```

The Deployment has 5.2's name, so this is a rolling update of the app that is
already there, not a second one. Watch it go — and note that it only reaches
`READY 1/1` if `/healthz` really is exempt from the password:

```shell
kubectl rollout status deployment/my-deployment -n snippet-letsencrypt-demo
kubectl get pods -n snippet-letsencrypt-demo
```

Check that nginx accepted the config. A syntax error keeps the container
crash-looping, and the reason is in the log rather than in any Kubernetes
status:

```shell
kubectl logs deploy/my-deployment -n snippet-letsencrypt-demo
```

## Test it

No credentials — `401`, with the realm *you* wrote this time:

```shell
curl -i https://my-app.example.com/
```

```
HTTP/2 401
www-authenticate: Basic realm="Restricted area"
```

The realm is the string from `nginx-conf.yml`, and that is how you can tell
the two examples apart from outside: 5.3.1 answers
`realm="https://my-app.example.com/"`, because Envoy builds it from the
request URI and offers no way to name it. (The `server:` header is no help —
Envoy overwrites it with its own on the way out, whoever produced the
response.)

With credentials, the welcome page is back:

```shell
curl -u alice https://my-app.example.com/
```

The exempt path answers with no password at all, which is the per-location
control 5.3.1 could not express:

```shell
curl https://my-app.example.com/healthz
```

```
ok
```

Worth being deliberate about: `/healthz` is routed from the internet like
every other path, so exempting it publishes it. That is fine for a two-byte
`ok` and not at all fine for a `/metrics` endpoint — pair `auth_basic off`
with `allow`/`deny` on the cluster's network range when the content is worth
something.

And a wrong password is refused by the app, so it is **in the app's log** —
with the username nginx authenticated, since `$remote_user` is part of the
stock log format:

```shell
curl -i -u alice:wrong https://my-app.example.com/

kubectl logs deploy/my-deployment -n snippet-letsencrypt-demo --tail=5
```

```
10.42.0.9 - - [16/Sep/2026:09:12:44 +0000] "GET / HTTP/1.1" 401 179 "-" "curl/8.5.0" "203.0.113.7"
10.42.0.9 - alice [16/Sep/2026:09:12:51 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.5.0" "203.0.113.7"
```

The third field is `$remote_user`, empty on the refused request and `alice` on
the accepted one. The client address is the Gateway's Pod, the real one having
been pushed into `X-Forwarded-For` — which is the usual consequence of running
behind a proxy, and unrelated to the password.

In 5.3.1 those lines are in the Envoy Gateway proxy's log, in another
namespace, under a name generated by the controller. Here they are one
`kubectl logs` away, next to the request they are about — a small thing that
makes a real difference the day someone asks *who got in, and when*.

The redirect on port 80 still answers without a password, as before:

```shell
curl -i http://my-app.example.com/
```

Not because of any care taken in the manifests, this time: the redirect never
reaches nginx.

## Changing the password, changing the rules

Two different operations here, with two different costs — a distinction 5.3.1
does not have, since it has nothing but a policy.

**The password: no restart.** nginx opens the htpasswd file on every request,
and the kubelet refreshes a mounted Secret a minute or two after it changes
(its sync period, plus cache propagation). So:

```shell
htpasswd -B .htpasswd alice      # or -D bob to remove a user

kubectl create secret generic basic-auth-users \
  --from-file=.htpasswd \
  -n snippet-letsencrypt-demo \
  --dry-run=client -o yaml | kubectl apply -f -
```

and a minute or two later the old password stops working, with nothing
restarted. Watch it happen:

```shell
watch -n5 'curl -s -o /dev/null -w "%{http_code}\n" -u alice:OLDPASSWORD https://my-app.example.com/'
```

**The config: a restart.** The mounted ConfigMap is refreshed on the same
schedule, but nginx only reads its configuration at startup and nothing tells
it to reload. After editing `nginx-conf.yml`:

```shell
kubectl apply -f nginx-conf.yml -n snippet-letsencrypt-demo
kubectl rollout restart deployment/my-deployment -n snippet-letsencrypt-demo
```

That restart is the cost this approach carries and 5.3.1 does not: changing
who may enter touches a Secret in both cases, but changing *how* means
redeploying the app.

## When it does not work

- **The Pod never becomes Ready, the rollout hangs, and the site still works.**
  The probe is getting a `401`: the `location = /healthz` block is missing,
  misspelled, or lost its `auth_basic off`. `kubectl describe pod` shows
  `Readiness probe failed: HTTP probe failed with statuscode: 401`. The old
  Pod keeps serving the unprotected page in the meantime, which is a rollout
  behaving exactly as it should and a demo appearing to do nothing. This is
  the failure mode this example was built to show.
- **`500 Internal Server Error` on every request, with the right password.**
  nginx cannot read the htpasswd file. `kubectl logs` says
  `open() "/etc/nginx/secrets/.htpasswd" failed (13: Permission denied)` —
  the workers run as the unprivileged `nginx` user and the Secret is mounted
  `0400` root-owned. Use `0444`, or `fsGroup: 101` with `0440`.
- **The new Pod never becomes Ready either, but with `connection refused`.**
  nginx started with no `server` block at all: the ConfigMap key does not end
  in `.conf`, so the image's `include /etc/nginx/conf.d/*.conf` matched
  nothing — and the mount had already replaced the directory holding the
  original `default.conf`. nginx runs happily, listening on nothing; the
  probe cannot connect and the Gateway answers `503`. The key must end in
  `.conf`.
- **`404 Not Found` instead of the page, once logged in.** The mount replaced
  the whole `conf.d` directory, so the `root` directive has to be in *your*
  server block — without it nginx falls back to its compiled-in default,
  which is not where the welcome page lives. It is in `nginx-conf.yml`; check
  it survived your edits.
- **Every login fails, with `crypt_r() failed` in the log.** The container's
  `crypt()` does not know the hash format. Regenerate with `-m` (`$apr1$`),
  which nginx implements itself and never delegates.
- **`401`, but the realm is the URL instead of `Restricted area`.** 5.3.1's
  SecurityPolicy is still applied and is answering first. Delete it (see
  *Prerequisites*).

## Remove the demo

Put the app back the way 5.2 left it — no password, stock config:

```shell
kubectl delete -f nginx-conf.yml -n snippet-letsencrypt-demo
kubectl apply -f ../5.2_lets_encrypt/deployment.yml -n snippet-letsencrypt-demo
kubectl delete secret basic-auth-users -n snippet-letsencrypt-demo
rm -f .htpasswd
```

Re-applying 5.2's Deployment is what removes the volumes and the probe;
deleting `deployment.yml` here would delete the app instead.

```shell
kubectl rollout status deployment/my-deployment -n snippet-letsencrypt-demo
curl -i https://my-app.example.com/
```

To remove the rest — the app, the Gateway, the certificate, the namespace, the
ClusterIssuers, the DNS record and the shared cluster add-ons — follow
[5.2's *Remove the demo*](../5.2_lets_encrypt/README.md#remove-the-demo)
section, which is where those resources come from.

## Which one to use

None of the three is the right answer in general, which is why all three are
here.

**At the Gateway (5.3.1)** when the app is a black box you do not control — a
stock image, a vendor's container, something you would rather not rebuild —
when several backends behind the same route need the same gate, or when the
app must simply never be exposed to unauthenticated requests.

**In the web server (5.3.2)** when you already ship the app's configuration,
when you need a decent hash, a chosen realm or an exempt path, or when the
manifests have to survive a change of ingress controller. This is also the
one that keeps working when the app moves off Kubernetes entirely: the same
two nginx directives run in a `docker compose` stack or on a plain VM.

**In application code**
([`6.3.1_stateless_backend_and_basic_auth_in_fastapi`](../6.3.1_stateless_backend_and_basic_auth_in_fastapi/))
when the answer depends on *who* is asking — per-user data, roles, an audit
trail. That is a different problem, and htpasswd stops being the right shape
for it well before you get there.
