# Secret

A Secret stores sensitive data (passwords, tokens, keys) as key/value pairs,
decoupled from the container image. It works exactly like a ConfigMap
(c.f. [1.3_config_map](../1.3_config_map)) and Pods consume it the same way —
as environment variables or as files mounted in a volume — but Kubernetes
stores its values base64-encoded and only mounts it in memory (tmpfs) when
used as a volume. Note that base64 is an encoding, not encryption: anyone
with read access to the Secret (or to etcd) can decode it. C.f.
[Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/secret/).

Here the Secret holds two entries, `message1` and `message2` (defined via
`stringData`, so they are given here in plain text and Kubernetes
base64-encodes them on creation), and three Pod variants show the different
ways to consume them.


## Namespace

Create the namespace for the demo: `kubectl create namespace snippet-secret-demo`

Add `-n snippet-secret-demo` to every `kubectl` command below.


## Secret

Create the Secret: `kubectl apply -f secret.yml -n snippet-secret-demo`

Inspect it (values are base64-encoded): `kubectl get secret my-secret -n snippet-secret-demo -o yaml`

Decode a value: `kubectl get secret my-secret -n snippet-secret-demo -o jsonpath='{.data.message1}' | base64 -d`


## Env (all keys)

`envFrom` injects every key of the Secret as an environment variable, using
the key names as-is.

Deploy the Pod: `kubectl apply -f pod_env_all.yml -n snippet-secret-demo`

Check the environment variables inside the container:

`kubectl exec -it pod/my-pod -n snippet-secret-demo -- sh -c 'echo $message1'`

`kubectl exec -it pod/my-pod -n snippet-secret-demo -- sh -c 'echo $message2'`

Delete the Pod: `kubectl delete -f pod_env_all.yml -n snippet-secret-demo`


## Env (selected key)

`valueFrom.secretKeyRef` injects a single chosen key as an environment
variable under a name of your choice — here `message1` is exposed as `HELLO`.

Deploy the Pod: `kubectl apply -f pod_env_selected.yml -n snippet-secret-demo`

Check the environment variable inside the container:

`kubectl exec -it pod/my-pod -n snippet-secret-demo -- sh -c 'echo $HELLO'`

Delete the Pod: `kubectl delete -f pod_env_selected.yml -n snippet-secret-demo`


## Volume

Mounting the Secret as a volume creates one file per key under the mount
path, with the file content set to the corresponding decoded value.

Deploy the Pod: `kubectl apply -f pod_volume.yml -n snippet-secret-demo`

Check the mounted file inside the container:

`kubectl exec -it pod/my-pod -n snippet-secret-demo -- cat /etc/config/message1`

Delete the Pod: `kubectl delete -f pod_volume.yml -n snippet-secret-demo`


## Cleanup

Delete the Secret: `kubectl delete -f secret.yml -n snippet-secret-demo`

Delete the namespace: `kubectl delete namespace snippet-secret-demo`
