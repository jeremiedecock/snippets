# Your own image, pulled from a private registry (OVHcloud MPR)

This is [`6.1_private_docker_registry_ghcr`](../6.1_private_docker_registry_ghcr/)
with **GHCR replaced by the OVHcloud Managed Private Registry**: the same
three-line FastAPI app, the same `kubernetes.io/dockerconfigjson` Secret,
the same `imagePullSecrets` — only the registry, and the way credentials are
obtained from it, change.

The registry side is where the difference lies.
[**MPR**](https://www.ovhcloud.com/en/public-cloud/managed-private-registry/)
is a managed [**Harbor**](https://goharbor.io/), the CNCF registry, run for
you in an OVHcloud region. So instead of a GitHub account and a personal
access token, there are three things to get right, and they are Harbor
concepts rather than OVHcloud ones:

- a **project** — Harbor's namespace, the `build` in
  `.../build/hello:1.0`. Unlike GHCR, where the first `push` creates the
  package, nothing can be pushed until the project exists;
- a **robot account** — the machine identity you authenticate with. Not the
  admin account OVHcloud generates for you, and not a password: a name with
  a `$` in it and a token shown exactly once;
- the **registry host**, `<id>.<region>.container-registry.ovh.net`, which
  is both the Docker endpoint and the Harbor web UI.

Everything the cluster does with the result is unchanged from the GHCR
chapter, so this README does not re-explain the Secret in the same depth —
[`6.1_private_docker_registry_ghcr`](../6.1_private_docker_registry_ghcr/#4-create-the-pull-secret)
does that. It gives the full walkthrough, but spends its length on what is
specific to OVHcloud and Harbor.

## What is in this directory

| File | What it is |
| --- | --- |
| `main.py` | the whole application: a FastAPI app with one route, `GET /`, returning `{"message": "hello"}` |
| `Containerfile` | how to build it: `python:3.14-slim`, `pip install "fastapi[standard]==0.141.1"` (pinned, so that two builds of the same tag cannot differ), run `fastapi run` on port 8000 |
| `pod.yml` | a bare Pod (as in [`1.1_pod_only`](../1.1_pod_only/)) running that image, with `imagePullSecrets` |
| `secret.yml` | the pull Secret written as a manifest — shown for reference, **not** the one you should apply (see below) |

`main.py` and the `Containerfile` are byte-for-byte those of the GHCR
chapter; only `pod.yml` and `secret.yml` differ, and only in the registry
host, the image path and the Secret's name.

## How a private pull actually works

Three actors, and the order matters:

```
   you                    registry (Harbor @ OVHcloud)           cluster
   ---                    ----------------------------           -------
podman login  --robot$git + token-->  authenticates you
podman build
podman push   -------------------->   stores <id>.<region>....net/build/hello:1.0
                                            ^
                                            |  kubelet pulls, with the
                                            |  credentials found in the
                                            |  imagePullSecrets Secret
                                            +--------------- Pod scheduled
```

The image reference in `pod.yml` reads
`<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0`,
and each part is doing work:

- `<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net` — the **registry
  host**. The subdomain is not yours to choose: OVHcloud assigns it when the
  registry is created, and it encodes the registry's identifier and the
  region it runs in. Omit the host and the container runtime defaults to
  Docker Hub, which is why `nginx` worked without one in the earlier
  examples;
- `build` — the **Harbor project**. On GHCR this slot held a GitHub user or
  organisation; here it is an object you created yourself, with its own
  members, quota and visibility;
- `hello` — the repository, i.e. the image name;
- `1.0` — the **tag**. Prefer an explicit version over `latest`: `latest` is
  just a tag like any other, with no notion of "newest", and it makes it
  impossible to tell which build a Pod is running.

The pull is done by the **kubelet on the node**, not by `kubectl` and not
from your laptop. The credentials therefore have to be *in the cluster*,
which is what the Secret is for — and being a namespaced object, it has to
exist in the same namespace as the Pod that references it. Copy the app to a
second namespace and you copy the Secret too.

Note what the Secret is *not*: it is never mounted, never visible as a file
or an environment variable inside the container. Only the kubelet reads it,
and only to talk to the registry.

## Prerequisites

- **A container engine**: [Podman](https://podman.io/) below. Every command
  works with Docker as well — `docker` in place of `podman`, plus
  `-f Containerfile`, which Podman finds on its own but older Docker
  versions do not.
- **An OVHcloud Public Cloud project**, and a Managed Private Registry in
  it. Unlike GHCR, this is a paid, provisioned service: it has a region, a
  plan and a storage quota, and it does not exist until you create it —
  step 1 below.
- **A Kubernetes cluster** reachable with `kubectl`. It does not have to be
  OVHcloud's Managed Kubernetes; any cluster works, local ones included, as
  long as its nodes have outbound access to the registry host. (If you have
  put [IP restrictions](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/add-ip-restrictions)
  on the registry, the nodes' egress addresses have to be in the allow
  list — not yours.)

`<YOUR_REGISTRY_SUB_DOMAIN>` is a placeholder, in `pod.yml`, in `secret.yml`
and in every command below. It stands for the part of the address that is
yours alone — everything before `.container-registry.ovh.net` in the URL the
Control Panel hands you at step 1. Replace it everywhere before running
anything:

```shell
sed -i 's/<YOUR_REGISTRY_SUB_DOMAIN>/your-registry-id.c1.your-region/g' pod.yml
```

`secret.yml` keeps its placeholders on purpose — it is read, not applied
(see step 6). Two more names are yours to pick, and they are spelled `build`
and `git` throughout: the **Harbor project** created in step 2, and the
**robot account** created in step 3. Change them in `pod.yml` too if you
choose differently.

## 1. Create the registry, and get the admin account

From the [OVHcloud Control Panel](https://www.ovh.com/manager/), in the
`Public Cloud` section, following
[Creating a private registry](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/creation):

1. `Containers & Orchestration` → `Managed Private Registry` → **Create a
   private registry**;
2. pick a **region**, a **name**, and a **plan**. The plan sets the included
   storage and the number of parallel requests; the `M` and `L` ones also
   include **Trivy**, Harbor's vulnerability scanner, which is worth having
   the day you push something you did not write yourself;
3. wait for the status to become `OK` — provisioning takes a few minutes;
4. then, from the `...` menu, **Generate identification details**, and
   confirm.

That last step returns the **Harbor administrator account** — a user name, a
password, and the registry `url`. Write the password down: it is shown once,
and regenerating it is the only way back.

Two remarks about that URL. The Control Panel displays it as
`https://<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net`, and **the
`https://` prefix has to be dropped** in every `podman`/`docker` command and
in
`--docker-server`: those expect a host, not a URL. And the same address
serves both purposes — open it in a browser and you get the Harbor web UI,
where you log in with the account you have just generated.

> **The admin account is not what you push with.** It can do everything,
> including deleting the registry's contents, it belongs to a human, and it
> is shared by whoever has access to the Control Panel. Use it to configure
> Harbor — that is what the next two steps do — and authenticate everything
> else with the robot accounts of step 3.

## 2. Create a Harbor project

In the Harbor UI, `Projects` → **New Project**, as described in
[Managing users and projects](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/managing-users-projects).
The name is the one that will appear in every image reference —
`build` here.

Two settings matter:

- **Access level**. Leave it **private**, the default: *"Only users with
  proper privileges can read from this project"*. Ticking *public* would
  make every image in it pullable anonymously — and would make this whole
  chapter unnecessary, since a public project needs no pull Secret at all.
  Visibility on Harbor is a property of the **project**, not of each image:
  there is no such thing as one private repository inside a public project.
- **Storage quota**, in GiB. `-1` means no limit (beyond the plan's). A
  quota that is reached does not produce an authentication error but a
  refused push, which is a different thing to look for when it happens.

Nothing can be pushed before this exists: *"No images can be pushed to
Harbor before the project is created."* A push to a project that is not
there fails with an authorisation error rather than a "not found", which is
the single most confusing failure of this chapter — see the last section.

## 3. Create a robot account

This is the real subject of this chapter, and where OVHcloud MPR differs
most from GHCR. Harbor's machine identities are **robot accounts**: a
generated token, an explicit list of permissions, an expiry date, and a
name that carries a `$`. They come in two kinds.

**Project-level** — `Projects` → `build` → `Robot Accounts` → **New Robot
Account**
([Harbor docs](https://goharbor.io/docs/2.13.0/working-with-projects/project-configuration/create-robot-accounts/)).
The account can only ever touch that one project, and its name is
`<prefix><project_name>+<account_name>`, i.e. **`robot$build+git`** for an
account named `git` in project `build`.

**System-level** — `Administration` → `Robot Accounts` → **New Robot
Account**, available because the OVHcloud-generated account is a Harbor
administrator
([Harbor docs](https://goharbor.io/docs/2.13.0/administration/robot-accounts/)).
Its name has no project part — **`robot$git`** — and its permissions are
granted per project, or to all of them at once with **Cover all projects**.
This is the form used in the commands below.

Whichever kind, three things to get right:

| Field | What to put | Why |
| --- | --- | --- |
| **Name** | `git`, `ci`, `k8s-pull`… | short, and one per consumer: a leaked or expired token then costs you one pipeline, not all of them |
| **Expiration time** | 30 days by default | see the warning below. `Never Expired` exists in the dropdown |
| **Permissions** | `Pull Repository`, plus `Push Repository` only if this account pushes | *"The Push Repository permission must be assigned with the Pull Repository permission"* — push alone is not a valid selection |

On **Finish**, Harbor shows the **secret** — the token — once, with a button
to copy it or to export it as JSON. There is no way to display it again;
the only recovery is `Refresh Secret`, which invalidates the old one.

> **Two robot accounts is the better habit**, as two tokens were on GHCR.
> The account that builds and pushes from your machine or your CI needs
> `Pull` + `Push`; the one handed to the cluster only ever needs `Pull`.
> Giving the kubelet a token that can overwrite your tags buys nothing.
>
> **And mind the expiry.** Harbor defaults robot tokens to **30 days**
> (`Configuration` → `System Settings` → `Robot Token Expiration (Days)` for
> the global default). The day one dies, *new* pulls start failing with
> `401` while already-running Pods keep going happily — so the breakage
> surfaces at the next node reboot or rescheduling, long after the cause.
> `Never Expired` is the pragmatic choice for a demo and a bad one for
> production; a calendar reminder is the honest middle ground.

### The `$` in the user name, and your shell

The user name to authenticate with is the **full robot name, prefix
included**, exactly as Harbor displays it: `robot$git`, not `git`. That `$`
is a character in the name, not a variable — but your shell does not know
that, and inside double quotes `"robot$git"` expands `$git` to the empty
string and sends `robot` to the registry, which fails with a `401` that
looks like a wrong password. Either escape it or, better, use single quotes:

```shell
podman login ... -u 'robot$git'      # single quotes: nothing is expanded
podman login ... -u "robot\$git"     # double quotes: the $ must be escaped
```

In YAML and JSON — `secret.yml`, `--docker-username` — no such expansion
happens, and `robot$git` is written plainly.

## 4. Log in, build, and push

Export the robot token, so the commands below and the `kubectl create
secret` later on can pick it up:

```shell
export HARBOR_TOKEN=...
```

Log in, feeding the token on stdin rather than as an argument, so it stays
out of your shell history and out of the process list:

```shell
echo $HARBOR_TOKEN | podman login <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net \
  -u 'robot$git' --password-stdin
```

`Login Succeeded!` means the credentials are now cached on your machine, in
`${XDG_RUNTIME_DIR}/containers/auth.json` (Podman) or `~/.docker/config.json`
(Docker). That file is the exact format the Kubernetes Secret will hold.

Build it, following
[Creating and using a Docker image stored in an OVHcloud Managed Private
Registry](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/create-private-image).
The tag has to spell out the registry host *and* the Harbor project — that
is what tells `push` where to go:

```shell
podman build -t <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0 .
```

Optional, and worth doing once: run it locally, before any Kubernetes is
involved. If it is broken here, it will be broken in the cluster too, and
far less pleasant to debug:

```shell
podman run -p 8000:8000 <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0
```

Open `http://localhost:8000` in a browser to see the FastAPI welcome message
(`{"message":"hello"}`), or `http://localhost:8000/docs` for the interactive
documentation FastAPI generates on its own. `Ctrl+C` to stop.

Push it:

```shell
podman push <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0
```

And check the result in the Harbor UI: `Projects` → `build` →
`Repositories` shows `build/hello`, with the `1.0` tag, its digest, its size
and — on the `M` and `L` plans — the Trivy scan of its layers.

## 5. Create the namespace

```shell
kubectl create namespace snippet-registry-ovh-demo
```

Add `-n snippet-registry-ovh-demo` to every `kubectl` command below.

## 6. Create the pull Secret

`kubectl` has a dedicated Secret type for this, which builds the
`dockerconfigjson` payload for you
([OVHcloud's own walkthrough](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/kubernetes)
uses the same command):

```shell
kubectl create secret docker-registry ovh-mpr-secret \
  --docker-server=<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net \
  --docker-username='robot$git' \
  --docker-password="$HARBOR_TOKEN" \
  -n snippet-registry-ovh-demo
```

- `--docker-server` must match the registry host in the image reference,
  **exactly**: the bare host, with no `https://` — the form the Control
  Panel shows — and no `/build` project path. A mismatch is not an error:
  the Secret is created, simply never matched against the pull, and the pull
  fails as if no credentials existed;
- `--docker-username` is the full robot name, `robot$git`, in single quotes;
- `--docker-password` takes the robot **token**, never the administrator
  password from step 1;
- `--docker-email` is accepted and ignored; it is a leftover from the
  original Docker Hub API.

Decode what was produced, and you get the same JSON your `podman login`
wrote on disk:

```shell
kubectl get secret ovh-mpr-secret -n snippet-registry-ovh-demo \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d
```

```json
{"auths":{"<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net":{"username":"robot$git","password":"...","auth":"cm9ib3..."}}}
```

Which is the reminder from [`1.4.1_secret`](../1.4.1_secret/), in its most
concrete form: the token is sitting there in plain text, base64 being an
encoding and not encryption. `auth` is just `base64(username:password)`.
Anyone able to read Secrets in this namespace holds that robot account —
hence the pull-only second account suggested above, and, for the real
answers, a dedicated secret-management tool (SOPS, Sealed Secrets, an
external secret store) plus encryption at rest on the cluster side.

### About `secret.yml`

`secret.yml` is the same object written declaratively, and it is here to be
read rather than applied:

```yaml
type: kubernetes.io/dockerconfigjson
stringData:
  .dockerconfigjson: |
    {
      "auths": {
        "<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net": {
          "username": "robot$<YOUR_ROBOT_ACCOUNT_NAME>",
          "password": "<YOUR_ROBOT_ACCOUNT_TOKEN>"
        }
      }
    }
```

Two things worth taking from it. First, `username`/`password` is enough —
Kubernetes does not require the precomputed `auth` field that `kubectl`
generates. Second, and the reason the imperative command is the one in the
walkthrough: filling this file in means **writing your robot token into a
file that sits next to your manifests**, one `git add` away from being
published forever. If you do want the manifest form — for GitOps, where
nothing is applied by hand — generate it instead of editing it, and then
encrypt it (with SOPS, or Sealed Secrets):

```shell
kubectl create secret docker-registry ovh-mpr-secret \
  --docker-server=<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net \
  --docker-username='robot$git' \
  --docker-password="$HARBOR_TOKEN" \
  --dry-run=client -o yaml > secret.yml
```

## 7. Deploy the Pod

```shell
kubectl apply -f pod.yml -n snippet-registry-ovh-demo
```

Two fields in `pod.yml` are new compared to `1.1_pod_only`:

```yaml
spec:
  containers:
    - image: <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0
      imagePullPolicy: Always
  imagePullSecrets:
    - name: ovh-mpr-secret
```

- **`imagePullSecrets`** is a list, and a list of *names* — the Secret has
  to exist in the Pod's namespace. Nothing validates it: a typo here
  produces a Pod that stays `ImagePullBackOff`, with the registry's `401` as
  the only clue.
- **`imagePullPolicy: Always`** makes the kubelet re-check the registry on
  every Pod start instead of trusting a cached layer. With an immutable tag
  it is redundant; while iterating on a mutable one it saves the confusion
  of a Pod that keeps running yesterday's code. (`IfNotPresent` is the
  default, except for `:latest`, where `Always` is implied.)

Watch it start. The image has to be downloaded first, so the Pod goes
through `ContainerCreating` for a few seconds:

```shell
kubectl get pods -n snippet-registry-ovh-demo --watch
```

`kubectl describe` is where the pull is visible — the `Events` section at
the bottom is the first thing to read whenever an image is involved:

```shell
kubectl describe pod my-pod -n snippet-registry-ovh-demo
```

```
Normal  Pulling  ...  Pulling image "<YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0"
Normal  Pulled   ...  Successfully pulled image "<YOUR_REGISTRY_SUB..." in 4.512s
Normal  Created  ...  Created container my-container
Normal  Started  ...  Started container my-container
```

The application's own logs, i.e. the FastAPI CLI and uvicorn starting up:

```shell
kubectl logs my-pod -n snippet-registry-ovh-demo
```

Then reach it. As in `1.1_pod_only`, the Pod IP is internal, so forward the
port to your machine:

```shell
kubectl port-forward my-pod 8000:8000 -n snippet-registry-ovh-demo
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
kubectl describe pod my-pod -n snippet-registry-ovh-demo | tail -20
```

- **`401 Unauthorized`** — the credentials were not accepted, or not found.
  In order of likelihood, and the first two are specific to Harbor: the user
  name lost its prefix or its `$` to the shell (it must reach the registry
  as `robot$git`, or `robot$build+git` for a project-level account), the
  **robot token has expired** — 30 days by default, and nothing warns you —
  then the Secret is not in this namespace, its name does not match
  `imagePullSecrets`, or `--docker-server` is not exactly the bare registry
  host. Test the token from your machine, which rules out Kubernetes
  entirely:
  ```shell
  echo $HARBOR_TOKEN | podman login <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net \
    -u 'robot$git' --password-stdin
  ```
- **`unauthorized to access repository` on a *push*** — usually not
  authentication at all: it is what Harbor answers when the **project does
  not exist**, or when the robot account has no `Push Repository`
  permission on it (remember that push has to be granted together with
  pull). Check the spelling of `build` in the tag against the project list
  in the UI.
- **`denied: requested access to the resource is denied`** — the account
  authenticated, but its permission list does not cover this project. A
  system-level robot only reaches the projects it was explicitly granted,
  unless `Cover all projects` was ticked.
- **`project quota exceeded` / a push refused with a storage message** —
  the project's quota, not a credentials problem. Raise it in the project's
  `Configuration` tab, or delete old tags and let Harbor's garbage
  collection run.
- **The pull times out, or fails with a network error** — if the registry
  has [IP restrictions](https://docs.ovhcloud.com/en/guides/public-cloud/containers-orchestration/managed-private-registry/add-ip-restrictions),
  the allow list has to contain the **cluster nodes'** public egress
  addresses. Your workstation being allowed proves nothing about them.
- **`manifest unknown` / `404`** — the image or tag does not exist under
  that name. A typo, or a `push` that never completed. Confirm from outside:
  ```shell
  podman pull <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net/build/hello:1.0
  ```
- **`Secret "ovh-mpr-secret" not found`**, spelled out in the events — the
  Pod was applied to a namespace the Secret is not in. The single most
  common cause is a forgotten `-n snippet-registry-ovh-demo`.
- **The Pod runs, but `curl` returns nothing** — not a registry problem.
  `kubectl logs` and the `Containerfile` are the place to look: the app must
  listen on `0.0.0.0`, not `127.0.0.1`, or nothing outside the container can
  reach it.

> **Repeating `imagePullSecrets` on every Pod** gets old quickly, and it is
> easy to forget on the next manifest. The usual fix is to attach the Secret
> to the namespace's default ServiceAccount, which then injects it into
> every Pod created there:
> ```shell
> kubectl patch serviceaccount default -n snippet-registry-ovh-demo \
>   -p '{"imagePullSecrets":[{"name":"ovh-mpr-secret"}]}'
> ```
> Convenient, and slightly implicit: nothing in the manifests says where the
> credentials come from any more. The following examples keep the explicit
> form.

## Remove the demo

```shell
kubectl delete -f pod.yml -n snippet-registry-ovh-demo
kubectl delete secret ovh-mpr-secret -n snippet-registry-ovh-demo
kubectl delete namespace snippet-registry-ovh-demo
```

Deleting the namespace would have removed both objects anyway; they are
listed separately because the next examples reuse the namespace pattern and
not the objects.

On the registry side,
`podman logout <YOUR_REGISTRY_SUB_DOMAIN>.container-registry.ovh.net` drops
the cached credentials on your machine, and the robot account is
deleted from the Harbor UI — `Administration` → `Robot Accounts`, or the
project's `Robot Accounts` tab. Deleting the account is what actually
revokes the token; deleting the Secret only removes the cluster's copy of
it.

Note that removing a *tag* in Harbor does not free the storage: the blobs
stay until **garbage collection** runs
(`Administration` → `Clean Up` → `Garbage Collection`), which is worth
knowing the day a quota looks full of images you thought you had deleted.
And the registry itself keeps billing until it is deleted from the Control
Panel — it is a provisioned service, not a free package host like GHCR.

**Keep the image** if you intend to continue.
[`6.2.1`](../6.2.1_stateless_backend_ingress_traefik/),
[`6.2.2`](../6.2.2_stateless_backend_gateway_api_envoy_gateway/) and
[`6.4`](../6.4_stateless_fullstack_app/) run this same `main.py`, written
against the GHCR copy of it; on OVHcloud the only changes are the image
reference in the Deployment and the name of the pull Secret — everything
else in those chapters applies verbatim.
