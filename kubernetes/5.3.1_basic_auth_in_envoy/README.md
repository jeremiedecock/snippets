# Password-protecting the app with HTTP Basic auth (htpasswd), at the Gateway

This example **continues [`5.2_lets_encrypt`](../5.2_lets_encrypt/)** rather
than repeating it. 5.2 served the app over HTTPS with an automatically renewed
Let's Encrypt certificate; here the Gateway asks for a **username and
password** before letting anything through, checked against an **htpasswd**
file.

Its sibling [`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/)
asks for the *same* password on the *same* URL, but has nginx check it instead
of the Gateway. Read this one first: it is the shorter of the two, and it is
where the protocol itself is explained. The two are mutually exclusive on a
running cluster — pick one at a time.

Run 5.2 first and **do not remove it** — stop before its *Remove the demo*
section. Everything it deployed (the Deployment, the Service, the Gateway, the
two HTTPRoutes, the ClusterIssuers, the certificate) stays exactly as it is,
in the same namespace, under the same domain name. This directory adds one
manifest on top of that running demo.

The order of the two examples is not arbitrary. Basic auth sends the password
with **every single request**, merely base64-encoded — not encrypted, not
hashed. Over plain HTTP, anyone on the path reads it in clear text on the
first request. Basic auth without TLS is not weak protection, it is a
credential leak, so 5.2 is a genuine prerequisite rather than a nice extra.

## What changes compared to `5.2_lets_encrypt`

The app does not change, the certificate does not change, the routing does not
change — literally, since none of it is re-applied. This directory holds a
single manifest, `security-policy.yml`, and everything else it refers to is
already on the cluster.

| | `5.2` | `5.3.1` (here) |
| --- | --- | --- |
| Reaching the app | anyone with the URL | username + password required |
| Manifests applied | six | one, on top of 5.2's |
| New manifest | — | `security-policy.yml` |
| New Secret | — | `basic-auth-users` (the htpasswd file) |
| New tool | — | `htpasswd` (or `openssl`) |
| Where the check happens | nowhere | the Envoy proxy, before the app |
| Portable across Gateway API implementations | yes | **no** — see below |
| Hash algorithms accepted | — | **SHA-1 only** — see below |

So, two things are new:

1. a **Secret** holding an htpasswd file, created imperatively like the
   certificate Secret of `5.1_tls` was;
2. a **SecurityPolicy** (`security-policy.yml`) pointing the Gateway at that
   Secret and naming the route to protect — `my-route`, the HTTPRoute 5.2
   already applied.

Both go into 5.2's namespace, `snippet-letsencrypt-demo`: a SecurityPolicy can
only target a resource in its own namespace, and the Secret has to be there
too.

### The one that matters: this manifest is not portable

Every manifest up to 5.2 is standard Gateway API. Move them to Cilium, Istio
or Traefik and they work, the `controllerName` of the GatewayClass aside.

`security-policy.yml` is different: `SecurityPolicy` belongs to the
`gateway.envoyproxy.io` API group, an **Envoy Gateway extension**. The Gateway
API has no standard way to express authentication yet, so every implementation
invents its own: a `Middleware` for Traefik, an
`nginx.ingress.kubernetes.io/auth-*` annotation for ingress-nginx, an
`AuthorizationPolicy` for Istio. The concept below transfers; this file does
not.

That is the recurring trade-off of the Gateway API as it stands today:
routing is standardised, everything around it is not.

[`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/) is the way out of
that trade-off for this particular feature: it does the same check in the
application's own web server, with nothing but standard Kubernetes objects,
and therefore runs unchanged behind any implementation — at a cost detailed
there.

## How HTTP Basic auth works

It is one of the oldest things in HTTP ([RFC 7617](https://datatracker.ietf.org/doc/html/rfc7617)),
and small enough to describe completely:

1. the client asks for a page with no credentials;
2. the server answers **`401 Unauthorized`** with a
   `WWW-Authenticate: Basic realm="..."` header. The *realm* names the
   protected area — it is what a browser shows in its password dialog, and
   what tells it which stored credentials to reuse;
3. the client retries with an `Authorization` header holding
   `Basic ` + base64 of `username:password`;
4. the server checks the pair and either serves the page or answers 401 again.

Step 3 is worth seeing for yourself, because "base64" reads like a security
measure to nobody who has decoded one:

```shell
printf 'alice:s3cr3t' | base64
# YWxpY2U6czNjcjN0
echo 'YWxpY2U6czNjcjN0' | base64 -d
# alice:s3cr3t
```

There is no hashing, no nonce, no expiry and no challenge-response. The
password travels, in a recoverable form, on every request — which is the whole
argument for putting it inside TLS.

Two consequences follow, and they are not bugs to be fixed but properties to
accept:

- **there is no logout.** The browser keeps re-sending the credentials until
  it is closed. Nothing on the server can revoke them for the current session.
- **there are no sessions, and therefore no per-user state.** Every request
  stands alone. That is also why it scales trivially and needs no store.

Basic auth is the right tool for a staging environment, an internal
dashboard, a metrics endpoint, or a demo you do not want indexed — anywhere a
shared password among a handful of people is honest. For end users with
accounts, use OIDC (Envoy Gateway has a `SecurityPolicy` for that too) or
JWTs.

### Where the check happens

The Envoy proxy enforces it, before anything reaches the Pod:

```
internet --HTTPS--> Gateway (Envoy: TLS + password check) --HTTP--> Service --> Pods
```

The nginx Pod is still the unmodified image from 4.3.1, still the one 5.2
started, and knows nothing about any of it — it is not even restarted. The
contrast is with [`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/),
which moves the check into that same Pod, and with
[`6.3.1_stateless_backend_and_basic_auth_in_fastapi`](../6.3.1_stateless_backend_and_basic_auth_in_fastapi/),
which does it in application *code*.

None of the three is wrong. At the Gateway: nothing to code, one place to
change the password, and the application stays reusable — but it is
all-or-nothing per route, the app never learns who the user is (unless you ask
for it with `forwardUsernameHeader`, mentioned at the bottom of
`security-policy.yml`), and the manifest only works on Envoy Gateway. In the
web server: portable, per-path, any hash algorithm — but the app's
configuration is now part of the deployment. In the app code: per-user
behaviour, real accounts, a database — at the price of writing and
maintaining it.

## How htpasswd works

`htpasswd` is the password-file tool that ships with the Apache HTTP server.
The file it writes is plain text, one user per line:

```
alice:{SHA}JauGvtFJymypwcDV23yakTiN3qs=
bob:{SHA}Ys23Ag/5IOWqZCw9QGaVDdHwH00=
```

That is all there is: `username:hash`, with a prefix naming the algorithm. The
password itself is never stored. On each request the proxy hashes what the
client sent and compares.

### Choosing the algorithm — the trap

`htpasswd` supports several hashes, selected by flag:

| Flag | Algorithm | Prefix in the file | |
| --- | --- | --- | --- |
| *(none)* / `-m` | MD5 (APR1) | `$apr1$` | **the default** since Apache 2.2.18 |
| `-B` | bcrypt | `$2y$` | what you should use anywhere else; `-C` tunes its cost |
| `-2` / `-5` | SHA-256 / SHA-512 `crypt()` | `$5$` / `$6$` | Unix platforms |
| `-d` | `crypt()` | *(none)* | historical, silently truncates the password to 8 characters |
| `-s` | SHA-1 | `{SHA}` | unsalted, insecure by today's standards |

Read that table bottom-up, because **Envoy only supports `-s`**, the worst
entry in it. Both the [Envoy basic auth
filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/basic_auth_filter)
and [Envoy Gateway](https://gateway.envoyproxy.io/docs/tasks/security/basic-auth/)
state that SHA is the only format currently accepted.

So the flag is not optional here. Leave it out and `htpasswd` writes a
perfectly good MD5 file that Envoy cannot read: every login then fails with a
401, with nothing in the manifests, the policy status or the Gateway status to
suggest why. This is the single most likely way to lose an hour on this
example.

Being unsalted has a concrete consequence: two users with the same password
get the same hash, and the hashes are crackable offline against a wordlist at
enormous speed. So:

- use **long, random** passwords here (`openssl rand -base64 24`), not
  memorable ones — length is the only defence left;
- treat the file and the Secret as compromised material if they leak, and
  rotate;
- never reuse a password that protects anything else.

Which is a fair summary of basic auth generally: an access gate for things
that need one, not an identity system.

## Prerequisites

**[`5.2_lets_encrypt`](../5.2_lets_encrypt/), deployed and still running** —
including its own prerequisites (Envoy Gateway and the `eg` GatewayClass,
cert-manager with `config.gatewayAPI.enabled=true`, a cluster with a public IP
and a domain name you own). Follow it to the end, up to and including the
switch to the production issuer, and stop before *Remove the demo*.

Envoy Gateway must be the implementation in use, and not just any Gateway API
controller: `security-policy.yml` is its extension.

Check that 5.2 is still there before going further. The Gateway must be
`PROGRAMMED=True`, the certificate `READY=True`, and the two HTTPRoutes
present — in particular `my-route`, which the policy targets by name:

```shell
kubectl get gateway,httproute,certificate -n snippet-letsencrypt-demo
```

And the site must answer without a password, which is what the next sections
change:

```shell
curl -i https://my-app.example.com/
```

Use the domain you already put in 5.2's manifests wherever
`my-app.example.com` appears below. Nothing in this directory contains a
hostname, so there is no `sed` to run this time.

Plus one new tool, **`htpasswd`**, from the Apache utilities — packaged as
`apache2-utils` on Debian/Ubuntu, `httpd-tools` on Fedora/RHEL, `apache2` in
Homebrew. It is a convenience, not a requirement: an `openssl` one-liner
below produces the same file.

## Create the password file

Pick a password that deserves the name:

```shell
openssl rand -base64 24
```

Then create the file. `-c` creates it (and **truncates an existing one** —
leave it out for every user after the first), `-s` selects SHA-1, and omitting
`-b` makes `htpasswd` prompt for the password instead of reading it from the
command line, which keeps it out of your shell history:

```shell
htpasswd -c -s .htpasswd alice
```

Add a second user to the same file — same command without `-c`:

```shell
htpasswd -s .htpasswd bob
```

Without `htpasswd` installed, the format is simple enough to write by hand —
`{SHA}` followed by base64 of the SHA-1 of the password is literally all it
is. This appends one line in exactly that format (put your own password in
place of `s3cr3t`, and mind that it lands in your shell history):

```shell
{ printf 'alice:{SHA}'; printf '%s' 's3cr3t' | openssl sha1 -binary | openssl base64; } >> .htpasswd
```

Look at the result, and check that the hashes start with `{SHA}` and not
`$apr1$` (MD5) or `$2y$` (bcrypt) — this is the check that saves the hour:

```shell
cat .htpasswd
```

```
alice:{SHA}JauGvtFJymypwcDV23yakTiN3qs=
```

`.htpasswd` is listed in `.gitignore` here. Keep it that way.

## Put it in a Secret

Envoy Gateway reads the file from an ordinary `Opaque` Secret, under the key
`.htpasswd` — the name matters, the policy looks for exactly that key.
`--from-file` uses the file's own name as the key, which is why the local file
has to be called `.htpasswd` too (or be given the key explicitly, as
`--from-file=.htpasswd=/path/to/some-other-name`).

It goes into 5.2's namespace, which already exists — there is no namespace to
create here:

```shell
kubectl create secret generic basic-auth-users \
  --from-file=.htpasswd \
  -n snippet-letsencrypt-demo
```

Check the key is there and spelled right (`kubectl` shows sizes, not content):

```shell
kubectl describe secret basic-auth-users -n snippet-letsencrypt-demo
```

Read it back to be sure it is the file you meant, and that the hashes survived
intact:

```shell
kubectl get secret basic-auth-users -n snippet-letsencrypt-demo \
  -o jsonpath='{.data.\.htpasswd}' | base64 -d
```

As with the TLS Secret of 5.1, this is created imperatively on purpose. The
declarative equivalent exists, but a Secret's content is only base64-encoded,
so committing it would publish the hashes — see the `9_secret_git_*` examples
for the ways to actually keep a secret in git.

## Apply the policy

One manifest, into the namespace 5.2 is already running in:

```shell
kubectl apply -f security-policy.yml -n snippet-letsencrypt-demo
```

Nothing is restarted and nothing is re-issued: Envoy Gateway reconfigures the
running proxy in place, within a second or two.

Check the policy was accepted. `ACCEPTED` must be `True`; if the targeted
route does not exist or the name is misspelled, it is not, and no password is
ever asked for — an open door that looks exactly like a closed one:

```shell
kubectl get securitypolicy -n snippet-letsencrypt-demo
kubectl describe securitypolicy my-basic-auth -n snippet-letsencrypt-demo
```

The `status` names the route it attached to. It should be `my-route`, the one
from 5.2.

## Test it

Without credentials — `401`, where the very same URL served the nginx page a
minute ago, and the `www-authenticate` header telling the client what to do:

```shell
curl -i https://my-app.example.com/
```

```
HTTP/2 401
www-authenticate: Basic realm="https://my-app.example.com/"
```

Envoy builds that realm from the request URI; unlike Apache or nginx, it is
not something you get to name.

With them, the nginx welcome page is back. `-u` is `curl` doing steps 2 and 3
of the protocol on your behalf:

```shell
curl -u alice https://my-app.example.com/
```

Pass the header by hand to see that nothing else is going on — this is exactly
what `-u` sent:

```shell
curl -H "Authorization: Basic $(printf 'alice:s3cr3t' | base64)" https://my-app.example.com/
```

A wrong password gets the same `401` as no password at all, with no hint about
which half was wrong:

```shell
curl -i -u alice:wrong https://my-app.example.com/
```

Check that the redirect on port 80 still answers **without** asking for
anything — that is the SecurityPolicy targeting the route rather than the
Gateway. The browser is bounced to HTTPS first, and only then asked for a
password, so the credentials never touch the plaintext connection:

```shell
curl -i http://my-app.example.com/
```

The same reasoning protects the certificate: the ACME challenge that 5.2 set
up is served on that same unprotected port 80, so renewal in two months still
works. A policy attached to the Gateway instead would break it silently.

In a browser, open `https://my-app.example.com/`: a password dialog appears,
showing the realm. Enter the credentials and the page loads. Note that there
is no way to sign out short of closing the browser — the promised consequence
of a protocol with no sessions.

### Watch it on the wire, once

The point of the chapter, in one command. Run it against the **HTTP** port,
where nothing is encrypted, and the credentials are in the request for anyone
on the path to read:

```shell
curl -v -u alice:s3cr3t http://my-app.example.com/ 2>&1 | grep -i authorization
```

```
> Authorization: Basic YWxpY2U6czNjcjN0
```

The same request over HTTPS puts that header inside the TLS session, where it
belongs. (The Gateway answers the plain one with a 301 rather than serving
anything — but the header was still sent, and still readable. Once a password
has travelled in clear text, it is spent.)

## Changing the password

Edit the file, replace the Secret, done. No restart: Envoy Gateway watches the
Secret and reconfigures the proxy in place, exactly as it does for the
certificate:

```shell
htpasswd -s .htpasswd alice

kubectl create secret generic basic-auth-users \
  --from-file=.htpasswd \
  -n snippet-letsencrypt-demo \
  --dry-run=client -o yaml | kubectl apply -f -
```

Removing a user is the same operation:

```shell
htpasswd -D .htpasswd bob
```

Every client using the old password starts getting 401s within seconds, which
is the only revocation basic auth has.

## When it does not work

- **Every login fails, including the right one.** The hashes are not SHA-1.
  `cat .htpasswd` and look for `{SHA}` — `$apr1$` means MD5 (what you get by
  forgetting the flag), `$2y$` means bcrypt, and Envoy reads neither.
  Regenerate with `-s`.
- **No password is ever asked for.** The policy is not attached. Check
  `ACCEPTED` in `kubectl describe securitypolicy`: usually the route name in
  `targetRefs` does not match the HTTPRoute 5.2 applied (`my-route`), or the
  policy was applied to another namespace than the route
  (`snippet-letsencrypt-demo`).
- **`401` even with correct credentials, and the policy is accepted.** The
  Secret key is wrong. It must be exactly `.htpasswd`; `kubectl describe
  secret basic-auth-users -n snippet-letsencrypt-demo` shows the key names.
- **The certificate stops renewing, two months in.** The policy is attached to
  the Gateway rather than the route, so the ACME challenge gets a 401 too.
  Target the HTTPRoute, or switch the issuer to a DNS-01 solver. Everything
  else in [5.2's troubleshooting](../5.2_lets_encrypt/README.md#when-it-does-not-work)
  still applies, since 5.2 is what is running underneath.

## Remove the demo

Removing what this directory added puts the cluster back in 5.2's state — the
app answering over HTTPS, without a password:

```shell
kubectl delete -f security-policy.yml -n snippet-letsencrypt-demo
kubectl delete secret basic-auth-users -n snippet-letsencrypt-demo
rm -f .htpasswd
```

```shell
curl -i https://my-app.example.com/
```

Keep the `.htpasswd` file if you are going on to
[`5.3.2_basic_auth_in_nginx`](../5.3.2_basic_auth_in_nginx/): it reuses the
same password file, and the same Secret, in the same namespace. Do delete the
SecurityPolicy, though — two independent 401 gates on one URL make for a
confusing demo.

To remove the rest — the app, the Gateway, the certificate, the namespace, the
ClusterIssuers, the DNS record and the shared cluster add-ons — follow
[5.2's *Remove the demo*](../5.2_lets_encrypt/README.md#remove-the-demo)
section, which is where those resources come from.
