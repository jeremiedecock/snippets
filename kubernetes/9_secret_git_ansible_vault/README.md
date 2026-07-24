# Ansible Vault

Same goal as `9_secret_git_sealed_secret` — never commit a secret in
plaintext — but with [Ansible
Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html) instead
of Sealed Secrets, and with Ansible replacing `kubectl apply` as the
deployment tool. Same app and same image as `9_secret_base64`
(`hello-fastapi:3.0`): nothing to rebuild.

**Read the "Is this a good idea?" section at the end before adopting this in
production** — it is a legitimate approach, but a minority one in the
Kubernetes world, and its trade-offs are structural.

## How it works

The token is stored **encrypted** in `vars/secrets.yml`, the playbook renders
`manifests/secret.yml.j2` with the decrypted value and sends the result
straight to the Kubernetes API. The plaintext only ever exists in memory,
during the run.

```
vars/secrets.yml (AES-256)  →  secret.yml.j2  →  Kubernetes API
       ↑ committed to git         ↑ template        ↑ real Secret object
```

Note that only the *value* is encrypted, not the whole file
(`ansible-vault encrypt_string`, not `ansible-vault encrypt`): variable names
stay readable, so `git diff` and code review still show *which* secret
changed. Encrypting the entire file turns every change into one opaque blob —
common, but worse for review.

The non-sensitive manifests (`manifests/*.yml`) are unchanged from
`9_secret_base64`, including `deployment.yml`: the app never knows how its
Secret was produced.

## Setup

```
pip install ansible-core kubernetes
ansible-galaxy collection install kubernetes.core
```

(`kubernetes` is the Python client used by the `kubernetes.core` modules; they
reuse the same kubeconfig as `kubectl`.)

The vault password for this example is **`demo-vault-password`** — obviously a
demo value, just like the fake token it protects. Write it to the file that
`ansible.cfg` and the commands below expect (it is in `.gitignore`, and must
never be committed — it decrypts everything):

```
printf 'demo-vault-password' > .vault_pass
chmod 600 .vault_pass
```

Real setups keep that password in a password manager, and inject it in CI from
the runner's secret store. `--vault-id prod@prompt` lets you use a distinct
password per environment.

## Deploy

```
ansible-playbook deploy.yml --vault-password-file .vault_pass
```

Use it: `kubectl port-forward service/hello 8080:80`, then
`curl http://localhost:8080/` → the token appears, exactly as in
`9_secret_base64`.

Read the encrypted value (this is what "the password decrypts everything"
means in practice):

```
ansible-vault view vars/secrets.yml --vault-password-file .vault_pass
```

Change it, and redeploy — Ansible opens `$EDITOR` on the decrypted content and
re-encrypts on save:

```
ansible-vault edit vars/secrets.yml --vault-password-file .vault_pass
```

To encrypt a *new* value:

```
ansible-vault encrypt_string --vault-password-file .vault_pass 'my-new-token' --name 'hello_token'
```

To rotate the vault password itself, `ansible-vault rekey vars/secrets.yml` —
which re-encrypts, but does **not** change the secret values: anyone who saw
the old password has already read them, so a leak means rotating the tokens
too.

Note the `no_log: true` on the Secret task in `deploy.yml`. Without it, the
decrypted token is printed by any `-v` run or failed task, and lands in the CI
logs — the classic way to leak a secret with this approach.

Remove everything: `ansible-playbook undeploy.yml`

## Is this a good idea?

**Short answer**: it is a sound approach *if Ansible is already your
deployment control plane*, and a poor default otherwise. It is not an
anti-pattern, but it is not the Kubernetes-native answer either.

The structural difference with Sealed Secrets is the cryptography, and
everything else follows from it:

| | Ansible Vault | Sealed Secrets |
| --- | --- | --- |
| Cryptography | **symmetric** (one shared password) | **asymmetric** (public/private keys) |
| Who can encrypt | whoever can also decrypt | anyone, including CI, with the public key |
| Who can decrypt | anyone holding the password | only the in-cluster controller |
| Portable across clusters | yes (it is just a file) | no (bound to one controller's key) |
| Deployment model | **push** (someone runs the playbook) | **pull**, GitOps-compatible |

The consequences worth weighing:

- **No write-only capability.** With Sealed Secrets or External Secrets, a
  developer or a CI job can *add* a secret without being able to read the
  existing ones. With Vault's symmetric password, anyone who can deploy can
  read every secret in the repo. That scales badly beyond a small, trusted
  team.
- **Incompatible with GitOps.** Argo CD and Flux reconcile the cluster by
  pulling from git; neither can decrypt an Ansible Vault file. Both integrate
  SOPS natively. If you might adopt a GitOps controller later, this approach
  does not carry over — SOPS does, and offers the same "encrypted values in
  git" model (with age/KMS/PGP keys instead of a shared password).
- **It does not solve encryption at rest in etcd** — no more than Sealed
  Secrets or SOPS does. That part is orthogonal, still needed, and treated in
  `9_secret_etcd_encryption_at_rest`.
- **The password is a single point of failure**, and rotating it properly
  means rotating the secrets themselves.

**How common is it?** Common in Ansible-centric shops, in homelabs and in
small teams — typically where the same playbooks already provision the VMs,
install k3s and configure DNS, and where adding one more play is far simpler
than introducing a new controller. It is rare in Kubernetes-native or GitOps
organisations, where SOPS, Sealed Secrets and External Secrets dominate. So:
a legitimate and well-understood minority pattern, not a mainstream Kubernetes
practice.

**Where it is genuinely the right tool**: bootstrapping. Something has to
create the very first credentials of a cluster — including installing the
Sealed Secrets controller and restoring its private key from backup. Ansible
with Vault is excellent for that, and then application secrets can be handed
over to a Kubernetes-native mechanism. The two approaches compose more often
than they compete.

**Recommendation**: if you already run Ansible and have no GitOps controller,
this is fine — keep `encrypt_string` (not whole-file encryption), `no_log`,
and a per-environment `--vault-id`. If you are starting fresh, or use Argo CD
or Flux, prefer SOPS (closest equivalent, GitOps-native) or Sealed Secrets
(`9_secret_git_sealed_secret`). If you already run Vault or a cloud
secret manager, prefer External Secrets Operator.
