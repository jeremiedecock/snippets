# Your own image, pulled from a private registry (GHCR)

Every example so far ran a **stock public image** —
[nginx](https://hub.docker.com/_/nginx) from Docker Hub — which the cluster
pulls anonymously, with nothing to configure. From here on the app is
**your own code**: a three-line FastAPI service, built into an image, pushed
to a registry, and pulled back by the cluster.

That last step is where something new is needed. The image is published to
[**GHCR**](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry),
the GitHub Container Registry, and a package pushed there is **private by
default**: an anonymous `docker pull` gets a `401`, and so does the cluster.
So this example is really about one Kubernetes object — a
`kubernetes.io/dockerconfigjson` **Secret**, referenced from the Pod through
`imagePullSecrets` — plus the GitHub-side token it carries.

[`6.1_private_docker_registry_ovh`](../6.1_private_docker_registry_ovh/) is
this same example against the **OVHcloud Managed Private Registry** (a
managed Harbor) instead: same app, same Secret, different registry — and
robot accounts in place of the personal access token.

Everything after this directory reuses the image built here, so it is worth
getting to the end of it: the same `hello-fastapi:1.0` image is what
[`6.2.1_stateless_backend_ingress_traefik`](../6.2.1_stateless_backend_ingress_traefik/)
and [`6.2.2_stateless_backend_gateway_api_envoy_gateway`](../6.2.2_stateless_backend_gateway_api_envoy_gateway/)
put behind an Ingress and a Gateway, and what the frontend of
[`6.4_stateless_fullstack_app`](../6.4_stateless_fullstack_app/) talks to.

## What is in this directory

| File | What it is |
| --- | --- |
| `main.py` | the whole application: a FastAPI app with one route, `GET /`, returning `{"message": "hello"}` |
| `Containerfile` | how to build it: `python:3.14-slim`, `pip install "fastapi[standard]==0.141.1"` (pinned, so that two builds of the same tag cannot differ), run `fastapi run` on port 8000 |
| `pod.yml` | a bare Pod (as in [`1.1_pod_only`](../1.1_pod_only/)) running that image, with `imagePullSecrets` |
| `secret.yml` | the pull Secret written as a manifest — shown for reference, **not** the one you should apply (see below) |

A bare Pod on purpose: the new thing here is the image and its credentials,
and a Deployment would add nothing to that. `pod.yml` is otherwise the same
shape as the very first example.

## How a private pull actually works

Three actors, and the order matters:

```
   you                        registry (ghcr.io)                cluster
   ---                        ------------------                -------
podman login    --PAT-->   authenticates you
podman build
podman push     ------->   stores ghcr.io/<user>/hello-fastapi:1.0
                                     ^
                                     |  kubelet pulls, with the credentials
                                     |  found in the imagePullSecrets Secret
                                     +---------------------------- Pod scheduled
```

The image reference in `pod.yml` reads
`ghcr.io/jeremiedecock/hello-fastapi:1.0`, and each part is doing work:

- `ghcr.io` — the **registry host**. Omit it and the container runtime
  defaults to Docker Hub, which is why `nginx` worked without one in the
  earlier examples;
- `jeremiedecock` — the **namespace** on that registry; on GHCR, a GitHub
  user or organisation;
- `hello-fastapi` — the repository, i.e. the image name;
- `1.0` — the **tag**. Prefer an explicit version over `latest`: `latest` is
  just a tag like any other, with no notion of "newest", and it makes it
  impossible to tell which build a Pod is running.

The pull is done by the **kubelet on the node**, not by `kubectl` and not from
your laptop. The credentials therefore have to be *in the cluster*, which is
exactly what the Secret is for — and being a namespaced object, it has to
exist in the same namespace as the Pod that references it. Copy the app to a
second namespace and you copy the Secret too.

Note what the Secret is *not*: it is never mounted, never visible as a file or
an environment variable inside the container. Only the kubelet reads it, and
only to talk to the registry.

## Prerequisites

- **A container engine**: [Podman](https://podman.io/) below. Every command
  works with Docker as well — `docker` in place of `podman`, plus
  `-f Containerfile`, which Podman finds on its own but older Docker
  versions do not.
- **A GitHub account**, and nothing else on the GHCR side: the registry
  needs no prior setup, the package is created by the first `push`.
- **A Kubernetes cluster** reachable with `kubectl`. Anything works here,
  local clusters included — the cluster only needs outbound access to
  `ghcr.io`, not a public address.

Replace `jeremiedecock` with your own GitHub username everywhere, in the
commands below and in `pod.yml`:

```shell
sed -i 's/jeremiedecock/your-github-username/g' pod.yml
```

## 1. Create a Personal Access Token

GHCR does not use your GitHub password; it authenticates with a **PAT
(classic)**, as described in
[Authenticating with a personal access token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic).
Create it under *Settings → Developer settings → Personal access tokens →
Tokens (classic)*, with these scopes:

| Scope | What it allows | Needed by |
| --- | --- | --- |
| `read:packages` | pull images | the **cluster**, and you |
| `write:packages` | push images | you |
| `delete:packages` | delete a published version | you, at cleanup time |
| `repo` | link a package to a private repository | you, if the source repo is private |

Copy it as soon as GitHub shows it — the value is displayed once. Export it
from your `.bashrc` so the commands below (and the `kubectl create secret`
later on) can pick it up:

```shell
export GHCR_TOKEN=ghp_...
```

Then log in, feeding the token on stdin rather than as an argument, so it
stays out of your shell history and out of the process list:

```shell
echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin
```

`Login Succeeded!` means the credentials are now cached on your machine, in
`${XDG_RUNTIME_DIR}/containers/auth.json` (Podman) or `~/.docker/config.json`
(Docker). That file is the exact format the Kubernetes Secret will hold.

> **Two tokens is the better habit.** The token above can push *and* delete,
> and the one handed to the cluster only ever needs `read:packages`. On
> anything but a demo, create a second, read-only token for the pull Secret,
> and give both an expiry date. Mind that expiry: the day the token dies,
> *new* pulls start failing with `401` while already-running Pods keep going
> happily, so the breakage surfaces at the next node reboot or rescheduling,
> long after the cause.

## 2. Build and push the image

Build it, following
[Pushing container images](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#pushing-container-images).
The tag has to spell out the destination registry and namespace — that is
what tells `push` where to go:

```shell
podman build -t ghcr.io/jeremiedecock/hello-fastapi:1.0 .
```

Optional, and worth doing once: run it locally, before any Kubernetes is
involved. If it is broken here, it will be broken in the cluster too, and far
less pleasant to debug:

```shell
podman run -p 8000:8000 ghcr.io/jeremiedecock/hello-fastapi:1.0
```

Open `http://localhost:8000` in a browser to see the FastAPI welcome message
(`{"message":"hello"}`), or `http://localhost:8000/docs` for the interactive
documentation FastAPI generates on its own. `Ctrl+C` to stop.

Push it:

```shell
podman push ghcr.io/jeremiedecock/hello-fastapi:1.0
```

And check the result on GitHub: <https://github.com/jeremiedecock?tab=packages>.
The package is there, marked **Private** — which is the whole point of the
next step. (A public package needs no Secret at all: remove
`imagePullSecrets` from `pod.yml` and the pull just works. The visibility is
changed from the package's *Package settings* page, and *"Private"* is the
default for a freshly pushed one.)

## 3. Create the namespace

```shell
kubectl create namespace snippet-registry-demo
```

Add `-n snippet-registry-demo` to every `kubectl` command below.

## 4. Create the pull Secret

`kubectl` has a dedicated Secret type for this, which builds the
`dockerconfigjson` payload for you:

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  -n snippet-registry-demo
```

- `--docker-server` must match the registry host in the image reference,
  `ghcr.io`, exactly. A mismatch (`https://ghcr.io`, or Docker Hub's
  `https://index.docker.io/v1/`) is not an error — the Secret is created,
  simply never matched against the pull, and the pull fails as if no
  credentials existed;
- `--docker-password` takes the **token**, never a GitHub password;
- `--docker-email` is accepted and ignored; it is a leftover from the
  original Docker Hub API.

Look at what was produced. The type is `kubernetes.io/dockerconfigjson`, and
the payload is a single key, `.dockerconfigjson`:

```shell
kubectl get secret ghcr-secret -n snippet-registry-demo -o yaml
```

Decode it, and you get the same JSON your `podman login` wrote on disk:

```shell
kubectl get secret ghcr-secret -n snippet-registry-demo \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d
```

```json
{"auths":{"ghcr.io":{"username":"jeremiedecock","password":"ghp_...","auth":"amVy...=="}}}
```

Which is the reminder from [`1.4.1_secret`](../1.4.1_secret/), in its most
concrete form: the token is sitting there in plain text, base64 being an
encoding and not encryption. `auth` is just `base64(username:password)`.
Anyone able to read Secrets in this namespace can push to your registry with
that token — hence the read-only second token suggested above, and, for the
real answers, a dedicated secret-management tool (SOPS, Sealed Secrets, an
external secret store) plus encryption at rest on the cluster side.

### About `secret.yml`

`secret.yml` is the same object written declaratively, and it is here to be
read rather than applied:

```yaml
type: kubernetes.io/dockerconfigjson
stringData:
  .dockerconfigjson: |
    { "auths": { "ghcr.io": { "username": "...", "password": "ghp_..." } } }
```

Two things worth taking from it. First, `username`/`password` is enough —
Kubernetes does not require the precomputed `auth` field that `kubectl`
generates. Second, and the reason the imperative command is the one in the
walkthrough: filling this file in means **writing your token into a file that
sits next to your manifests**, one `git add` away from being published
forever. If you do want the manifest form — for GitOps, where nothing is
applied by hand — generate it instead of editing it, and then encrypt it
(with SOPS, or Sealed Secrets):

```shell
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username='jeremiedecock' \
  --docker-password="$GHCR_TOKEN" \
  --dry-run=client -o yaml > secret.yml
```

## 5. Deploy the Pod

```shell
kubectl apply -f pod.yml -n snippet-registry-demo
```

Two fields in `pod.yml` are new compared to `1.1_pod_only`:

```yaml
spec:
  containers:
    - image: ghcr.io/jeremiedecock/hello-fastapi:1.0
      imagePullPolicy: Always
  imagePullSecrets:
    - name: ghcr-secret
```

- **`imagePullSecrets`** is a list, and a list of *names* — the Secret has to
  exist in the Pod's namespace. Nothing validates it: a typo here produces a
  Pod that stays `ImagePullBackOff`, with the registry's `401` as the only
  clue.
- **`imagePullPolicy: Always`** makes the kubelet re-check the registry on
  every Pod start instead of trusting a cached layer. With an immutable tag it
  is redundant; while iterating on a mutable one it saves the confusion of a
  Pod that keeps running yesterday's code. (`IfNotPresent` is the default,
  except for `:latest`, where `Always` is implied.)

Watch it start. The image has to be downloaded first, so the Pod goes through
`ContainerCreating` for a few seconds:

```shell
kubectl get pods -n snippet-registry-demo --watch
```

`kubectl describe` is where the pull is visible — the `Events` section at the
bottom is the first thing to read whenever an image is involved:

```shell
kubectl describe pod my-pod -n snippet-registry-demo
```

```
Normal  Pulling  ...  Pulling image "ghcr.io/jeremiedecock/hello-fastapi:1.0"
Normal  Pulled   ...  Successfully pulled image "ghcr.io/..." in 4.512s
Normal  Created  ...  Created container my-container
Normal  Started  ...  Started container my-container
```

The application's own logs, i.e. the FastAPI CLI and uvicorn starting up:

```shell
kubectl logs my-pod -n snippet-registry-demo
```

Then reach it. As in `1.1_pod_only`, the Pod IP is internal, so forward the
port to your machine:

```shell
kubectl port-forward my-pod 8000:8000 -n snippet-registry-demo
```

Open `http://localhost:8000` in a browser for the FastAPI welcome message —
the same response as the local `podman run`, this time served from the
cluster. `http://localhost:8000/docs` still works too, and
`kubectl logs -f` now shows a line per request.

## When it does not work

Image pull failures all look alike from `kubectl get pods`
(`ErrImagePull`, then `ImagePullBackOff` as the kubelet backs off and
retries). The distinguishing detail is always in the events:

```shell
kubectl describe pod my-pod -n snippet-registry-demo | tail -20
```

- **`401 Unauthorized`** — the credentials were not accepted, or not found.
  In order of likelihood: the Secret is not in this namespace, its name does
  not match `imagePullSecrets`, `--docker-server` is not exactly `ghcr.io`,
  the token lacks `read:packages`, or it has expired. Test the token from
  your machine, which rules out Kubernetes entirely:
  `echo $GHCR_TOKEN | podman login ghcr.io -u jeremiedecock --password-stdin`.
- **`denied` or `403 Forbidden`** — authentication worked, authorisation did
  not: usually a token that can read but whose account has no access to that
  package, or a package owned by an organisation with package permissions to
  grant.
- **`manifest unknown` / `404`** — the image or tag does not exist under that
  name. A typo in the username, or a `push` that never completed. Confirm
  from outside: `podman pull ghcr.io/jeremiedecock/hello-fastapi:1.0`.
- **`Secret "ghcr-secret" not found`**, spelled out in the events — the Pod
  was applied to a namespace the Secret is not in. The single most common
  cause is a forgotten `-n snippet-registry-demo`.
- **The Pod runs, but `curl` returns nothing** — not a registry problem.
  `kubectl logs` and the `Containerfile` are the place to look: the app must
  listen on `0.0.0.0`, not `127.0.0.1`, or nothing outside the container can
  reach it.

> **Repeating `imagePullSecrets` on every Pod** gets old quickly, and it is
> easy to forget on the next manifest. The usual fix is to attach the Secret
> to the namespace's default ServiceAccount, which then injects it into every
> Pod created there:
> ```shell
> kubectl patch serviceaccount default -n snippet-registry-demo \
>   -p '{"imagePullSecrets":[{"name":"ghcr-secret"}]}'
> ```
> Convenient, and slightly implicit: nothing in the manifests says where the
> credentials come from any more. The following examples keep the explicit
> form.

## Remove the demo

```shell
kubectl delete -f pod.yml -n snippet-registry-demo
kubectl delete secret ghcr-secret -n snippet-registry-demo
kubectl delete namespace snippet-registry-demo
```

Deleting the namespace would have removed both objects anyway; they are
listed separately because the next examples reuse the namespace pattern and
not the objects.

**Keep the image.** `ghcr.io/jeremiedecock/hello-fastapi:1.0` is the backend
of [`6.2.1`](../6.2.1_stateless_backend_ingress_traefik/),
[`6.2.2`](../6.2.2_stateless_backend_gateway_api_envoy_gateway/) and
[`6.4`](../6.4_stateless_fullstack_app/), and those three expect *this*
`main.py` behind the tag. The later examples, which run a modified app, give
it a tag of its own rather than overwriting this one — `4.0` and `5.0` for
the persistence chapters — which is the whole reason the
`Containerfile` pins its dependency and the tag is never reused. Only clean up
the registry side if you are stopping here — from the package's settings page on GitHub, or with
`podman logout ghcr.io` for the cached credentials on your machine.

Do revoke the PAT when you are done with it, from *Settings → Developer
settings → Personal access tokens*. A token with `write:packages` left
lying around in a shell history, a `.bashrc` and a Secret is the one piece
of this example with a real blast radius.
