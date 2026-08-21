# Copier template — Option 1: shared authentication directory (host bind-mount)

A [Copier](https://copier.readthedocs.io/) template that adds a containerized
(Podman) Claude Code environment to a project, where **all your projects share
a single authentication/state directory** on the host, bind-mounted into every
container. You authenticate **once**, for all projects — the same experience as
non-containerized Claude Code, where one `~/.claude` serves every project
directory on the machine.

This mirrors the official devcontainer guidance (a shared config volume
mounted on `~/.claude` + `CLAUDE_CONFIG_DIR` pointing at it):

- <https://code.claude.com/docs/en/devcontainer.md#persist-authentication-and-settings-across-rebuilds>
- <https://code.claude.com/docs/en/authentication.md#credential-management>

Two deviations from the official devcontainer recipe, both deliberate:

1. **Host directory instead of a named volume** (default
   `~/.config/claude-containers/`): the credentials survive
   `podman volume prune`, and the directory is easy to inspect and back up.
2. **Unique workspace path per project** (default `/workspace/<project_name>`):
   Claude Code keys its per-project state (history, `--continue`/`--resume`,
   folder trust, permissions) on the working directory path. With a shared
   config store, a unique path per project keeps that state separate — one
   shared login, isolated per-project state, exactly like on a host.

## Template layout

```
option1/                     <- the template (this directory)
├── copier.yml               <- questions & settings (not copied)
├── README.md                <- this file (not copied)
└── template/                <- rendered into the destination project
    ├── .copier-answers.yml.jinja
    ├── claude.sh.jinja
    └── containers/
        └── claude.containerfile
```

## Requirements

- [Copier](https://copier.readthedocs.io/) ≥ 9: `pipx install copier`
  (or `uv tool install copier`)
- Rootless Podman ≥ 4.3 (`--userns=keep-id:uid=...`)

## Creating a new project

```sh
copier copy /path/to/option1 /path/to/my-new-project
```

Copier asks the questions defined in `copier.yml`:

| Question              | Default                                          | Meaning                                        |
|-----------------------|--------------------------------------------------|------------------------------------------------|
| `project_name`        | *(required)*                                     | Image name, hostname, workspace path component |
| `image_name`          | `localhost/<project_name>:latest`                | Container image name                           |
| `container_workspace` | `/workspace/<project_name>`                      | Unique mount path of the project               |
| `claude_host_dir`     | `${XDG_CONFIG_HOME:-${HOME}/.config}/claude-containers` | Shared auth directory (same for ALL projects!) |

Generated files:

```
my-new-project/
├── .copier-answers.yml      <- your answers (enables `copier update`)
├── claude.sh                <- single entry point (build + auth + run)
└── containers/
    └── claude.containerfile
```

Then:

```sh
cd /path/to/my-new-project
./claude.sh        # first run builds the image; auth is asked only if the
                   # shared directory holds no token yet (once, for ALL projects)
```

### Adding the environment to an EXISTING project

Same command, pointing at the existing directory:

```sh
copier copy /path/to/option1 /path/to/existing-project
```

Only `claude.sh`, `containers/claude.containerfile` and `.copier-answers.yml`
are added; Copier asks before overwriting any conflicting file.

### Non-interactive generation

```sh
copier copy --defaults --data project_name=my-project \
    /path/to/option1 /path/to/my-project
```

`--defaults` accepts the default answers for every question not provided with
`--data`.

## Updating generated projects when the template evolves

`copier update` re-applies the (possibly newer) template while keeping your
answers, using the `.copier-answers.yml` recorded in the project. It requires
the template to be a **git repository with version tags**:

```sh
cd /path/to/option1
git init && git add -A && git commit -m "Claude Code container template, option 1"
git tag v1.0.0
```

then, in any generated project:

```sh
cd /path/to/my-project
copier update          # or: copier update --defaults
```

(Copying from a plain, non-git directory works too, but `copier update` will
not be available for projects generated that way.)

## Notes

- If `claude.sh` loses its executable bit during generation:
  `chmod +x claude.sh`.
- **The shared directory must be identical across projects** — that is what
  makes the login shared. Override at run time with `CLAUDE_CONTAINERS_DIR`
  (e.g. to test with a throwaway auth store).
- One-time migration from the previous per-project volume setup (of the
  `pytorch-autoencoders` repository) — seed the shared directory manually:

  ```sh
  mkdir -p ~/.config/claude-containers && chmod 700 ~/.config/claude-containers
  mp="$(podman volume inspect --format '{{.Mountpoint}}' pytorch-autoencoders-claude)"
  cp -a "$mp/." ~/.config/claude-containers/
  ```

- **Security**: any code running in any of these containers can read the
  shared token — the same trust model as non-containerized Claude Code. For
  projects running untrusted code, see Option 2 (isolated per-project state).
- **Concurrency**: several containers at once = several Claude Code terminals
  on one machine — supported.
- Reset auth (all projects): `rm -f ~/.config/claude-containers/.credentials.json`.

See the `option2` template for the alternative: a long-lived token generated
by `claude setup-token`, shared through an environment variable, with
per-project state volumes.
