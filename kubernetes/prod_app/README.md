# `prod_app` — application template

[Copier](https://copier.readthedocs.io/) template for a production fullstack
application (FastAPI backend + nginx frontend) published on the shared
Gateway of the cluster — either
[`../prod_common_DNS-01`](../prod_common_DNS-01/) (one wildcard certificate)
or [`../prod_common_HTTP-01`](../prod_common_HTTP-01/) (one certificate per
application).

One generated application = one namespace, one subdomain, one HTTPRoute. No
certificate, no redirect route and no Gateway change: the wildcard
certificate and the shared redirect of the infrastructure directory already
cover it.

## Use

```shell
pipx install copier          # or: uv tool install copier
copier copy prod_app ../invoices
cd ../invoices && git init && git add -A && git commit -m "Initial commit"
```

Then follow the generated `README.md`: `just login`, `just release`,
`just bootstrap`, `just deploy`.

### Updating a generated application later

```shell
cd ../invoices          # clean git working tree required
copier update           # re-applies the template diff, conflicts land as .rej
```

`copier update` only works if the **template itself** is a git repository
with tags — it needs a version to diff from, and records it as `_commit` in
`.copier-answers.yml`. Copied from a plain path, as above, it fails with
*"cannot obtain old template references"*.

To enable it, publish `prod_app/` as its own repository and tag releases:

```shell
git -C prod_app init && git -C prod_app add -A
git -C prod_app commit -m "Template v1.0.0" && git -C prod_app tag v1.0.0
copier copy /path/to/prod_app ../invoices     # or a git URL
```

Each template change then gets a new tag, and every application picks it up
with `copier update`.

## Questions asked

| Question | Default | Used for |
| --- | --- | --- |
| `app_slug` | — | namespace, image names, labels, HTTPRoute name |
| `app_title`, `app_description` | derived | the page and the OpenAPI title |
| `base_domain` | `example.com` | the domain the shared Gateway serves |
| `subdomain` | `app_slug` | → `subdomain.base_domain` |
| `namespace` | `app_slug` | one namespace per application |
| `api_prefix` | `/api` | path routed to the backend, stripped before forwarding |
| `registry`, `registry_owner`, `pull_secret` | `ghcr.io`, —, `ghcr-secret` | images and pull Secret |
| `version` | `0.1.0` | initial image tag |
| `backend_replicas`, `frontend_replicas` | `2` | |
| `gateway_name`, `gateway_namespace`, `gateway_listener` | `gateway-infra`, `gateway-infra`, `https` | must match the infrastructure directory — answer `https-<app_slug>` for `gateway_listener` on an **HTTP-01** cluster |

## What it generates

```
backend/src/main.py            GET / and GET /health
backend/src/requirements.txt   pinned
frontend/src/index.html        static page, fetches <api_prefix>/ relatively
containers/*.Containerfile     build context = repository root
kubernetes/                    namespace, http-route, pod-disruption-budgets
kubernetes/{backend,frontend}/ deployment + service
justfile                       build, push, bump, bootstrap, deploy, smoke
README.md                      deployment instructions for that application
.copier-answers.yml            enables `copier update`
```

Production defaults baked in: non-root containers with a read-only root
filesystem and dropped capabilities, resource requests and memory limits,
readiness *and* liveness probes, `maxUnavailable: 0` rollouts,
PodDisruptionBudgets, `app.kubernetes.io/*` labels.

## Conventions

- **One namespace per application**, holding both halves. The frontend and
  the backend are released together and their HTTPRoute forwards to Services
  in its own namespace, so no `ReferenceGrant` is involved.
- **Attaching to the shared Gateway is opt-in**: the namespace must carry
  `gateway-access: "true"`, which the cluster operator sets with
  `just grant <ns>` from the infrastructure directory. The generated
  `namespace.yml` carries
  the label for the single-team case — remove it when the two repositories
  have different owners.
- **`api_prefix` is stripped at the Gateway** and given back to uvicorn with
  `--root-path`, so the image stays neutral about where it is mounted. The
  filter and the flag are a matched pair.
- **Immutable tags.** `just bump` moves the version in the justfile and in
  both Deployments; the manifests are the source of truth for what runs.

## Editing the template

Jinja delimiters are `[[ ]]`, `[% %]` and `[# #]` (set in `copier.yml`), so
the generated `justfile` can use just's own `{{ }}` syntax untouched. Files
ending in `.jinja` are rendered and lose the suffix; every other file is
copied verbatim.

```shell
copier copy --defaults --data app_slug=demo --data registry_owner=acme \
  prod_app /tmp/demo-app        # render it somewhere disposable and read it
```
