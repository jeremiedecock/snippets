# ConfigMap

A ConfigMap stores non-sensitive configuration data (strings) as key/value
pairs, decoupled from the container image. Pods can consume it as
environment variables or as files mounted in a volume. C.f.
[Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/configmap/).

Here the ConfigMap holds two entries, `message1` and `message2`, and three
Pod variants show the different ways to consume them.


## Namespace

Create the namespace for the demo: `kubectl create namespace snippet-configmap-demo`


## ConfigMap

Create the ConfigMap: `kubectl apply -f configmap.yml -n snippet-configmap-demo`

Inspect it: `kubectl get configmap my-config-map -n snippet-configmap-demo -o yaml`


## Env (all keys)

`envFrom` injects every key of the ConfigMap as an environment variable,
using the key names as-is.

Deploy the Pod: `kubectl apply -f pod_env_all.yml -n snippet-configmap-demo`

Check the environment variables inside the container:

`kubectl exec -it pod/my-pod -n snippet-configmap-demo -- sh -c 'echo $message1'`

`kubectl exec -it pod/my-pod -n snippet-configmap-demo -- sh -c 'echo $message2'`

Delete the Pod: `kubectl delete -f pod_env_all.yml -n snippet-configmap-demo`


## Env (selected key)

`valueFrom.configMapKeyRef` injects a single chosen key as an environment
variable under a name of your choice — here `message1` is exposed as `HELLO`.

Deploy the Pod: `kubectl apply -f pod_env_selected.yml -n snippet-configmap-demo`

Check the environment variable inside the container:

`kubectl exec -it pod/my-pod -n snippet-configmap-demo -- sh -c 'echo $HELLO'`

Delete the Pod: `kubectl delete -f pod_env_selected.yml -n snippet-configmap-demo`


## Volume

Mounting the ConfigMap as a volume creates one file per key under the mount
path, with the file content set to the corresponding value.

Deploy the Pod: `kubectl apply -f pod_volume.yml -n snippet-configmap-demo`

Check the mounted file inside the container:

`kubectl exec -it pod/my-pod -n snippet-configmap-demo -- cat /etc/config/message1`

Delete the Pod: `kubectl delete -f pod_volume.yml -n snippet-configmap-demo`


## Cleanup

Delete the ConfigMap: `kubectl delete -f configmap.yml -n snippet-configmap-demo`

Delete the namespace: `kubectl delete namespace snippet-configmap-demo`
