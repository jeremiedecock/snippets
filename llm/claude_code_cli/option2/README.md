# Copier template — Option 2: long-lived OAuth token (`claude setup-token`)

A [Copier](https://copier.readthedocs.io/) template that adds a containerized
(Podman) Claude Code environment to a project, authenticated with a
**long-lived OAuth token** shared across projects through the
`CLAUDE_CODE_OAUTH_TOKEN` environment variable, while **each project keeps its
own isolated state volume** (history, sessions, folder trust, permissions).

`claude setup-token` performs the interactive OAuth procedure **once** and
generates a token valid **~1 year**. It works with a Claude **Pro/Max** (or
Team/Enterprise) subscription — this is subscription authentication, not an
API key — and is the mechanism the official docs recommend for CI and
Codespaces:

- <https://code.claude.com/docs/en/authentication.md#generate-a-long-lived-token>
- <https://code.claude.com/docs/en/authentication.md#authentication-precedence>
- <https://code.claude.com/docs/en/devcontainer.md#persist-authentication-and-settings-across-rebuilds>

## Template layout

```
option2/                     <- the template (this directory)
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
copier copy /path/to/option2 /path/to/my-new-project
```

Copier asks the questions defined in `copier.yml`:

| Question       | Default                                                  | Meaning                                  |
|----------------|----------------------------------------------------------|------------------------------------------|
| `project_name` | *(required)*                                             | Image name, hostname, volume name        |
| `image_name`   | `localhost/<project_name>:latest`                        | Container image name                     |
| `state_volume` | `<project_name>-claude`                                  | Per-project state volume (isolated)      |
| `token_file`   | `${XDG_CONFIG_HOME:-${HOME}/.config}/claude-containers/token` | Long-lived token file (shared by all) |

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
./claude.sh --setup-token   # once, for ALL projects: OAuth flow + paste the token
./claude.sh                 # no authentication question, ever
```

(If the token already exists — generated from another project or on the host —
skip `--setup-token`: it is read from the shared token file.)

### Adding the environment to an EXISTING project

Same command, pointing at the existing directory:

```sh
copier copy /path/to/option2 /path/to/existing-project
```

Only `claude.sh`, `containers/claude.containerfile` and `.copier-answers.yml`
are added; Copier asks before overwriting any conflicting file.

### Non-interactive generation

```sh
copier copy --defaults --data project_name=my-project \
    /path/to/option2 /path/to/my-project
```

`--defaults` accepts the default answers for every question not provided with
`--data`.

## Updating generated projects when the template evolves

`copier update` re-applies the (possibly newer) template while keeping your
answers, using the `.copier-answers.yml` recorded in the project. It requires
the template to be a **git repository with version tags**:

```sh
cd /path/to/option2
git init && git add -A && git commit -m "Claude Code container template, option 2"
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
- **Per-project isolation**: history, sessions and permissions never mix
  between projects — only the authentication is shared. This is the option to
  prefer if some projects run untrusted code
  (e.g. with `--dangerously-skip-permissions`).
- **Also works headless/CI**: the same token authenticates scripted
  `claude -p ...` runs where no interactive OAuth is possible.
- **The token is a plaintext secret** (mode 600): anyone holding it can use
  your subscription until it expires or is revoked. Keep it out of untrusted
  backups; never commit it.
- **Expiry**: after ~1 year, re-run `./claude.sh --setup-token`.
- **Precedence trap**: `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` take
  precedence over `CLAUDE_CODE_OAUTH_TOKEN` inside the container and would
  silently switch billing to the API. `claude.sh` only forwards the variables
  it explicitly lists, so a stray host `ANTHROPIC_API_KEY` is *not* forwarded.
- **A small per-project onboarding remains** (theme + folder trust, once per
  project). If you want zero questions on new projects too, that is what the
  Option 1 template (fully shared state directory) provides.

See the `option1` template for the alternative: a fully shared `~/.claude`
directory (one login *and* one shared state store, like non-containerized
Claude Code).
