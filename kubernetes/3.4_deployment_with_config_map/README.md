# Deployment with ConfigMap

Same ConfigMap as [1.3_config_map](../1.3_config_map), but consumed by a
Deployment (c.f. [3.2_deployment](../3.2_deployment)) instead of a bare Pod.
Each of the 2 replicas gets the same ConfigMap data, injected the same way it
would be for a single Pod — as environment variables or as files mounted in
a volume. C.f. [Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/configmap/).

Here the ConfigMap holds two entries, `message1` and `message2`, and three
Deployment variants show the different ways to consume them.


## Namespace

Create the namespace for the demo: `kubectl create namespace snippet-deployment-configmap-demo`

Add `-n snippet-deployment-configmap-demo` to every `kubectl` command below.


## ConfigMap

Create the ConfigMap: `kubectl apply -f configmap.yml -n snippet-deployment-configmap-demo`


## Env (all keys)

`envFrom` injects every key of the ConfigMap as an environment variable in
every replica's container, using the key names as-is.

Deploy: `kubectl apply -f deployment_env_all.yml -n snippet-deployment-configmap-demo`

Get the name of a Pod: `kubectl get pods -l app=my-app -n snippet-deployment-configmap-demo`

```
NAME                             READY   STATUS    RESTARTS   AGE
my-deployment-c5b59bdbf-s8m7h   1/1     Running   0          6s
my-deployment-c5b59bdbf-x826m   1/1     Running   0          6s
```

Check the environment variables inside that Pod (replace the name below with
one from the output above):

`kubectl exec -it pod/my-deployment-c5b59bdbf-s8m7h -n snippet-deployment-configmap-demo -- sh -c 'echo $message1'`

`kubectl exec -it pod/my-deployment-c5b59bdbf-s8m7h -n snippet-deployment-configmap-demo -- sh -c 'echo $message2'`

Delete: `kubectl delete -f deployment_env_all.yml -n snippet-deployment-configmap-demo`


## Env (selected key)

`valueFrom.configMapKeyRef` injects a single chosen key as an environment
variable under a name of your choice — here `message1` is exposed as `HELLO`.

Deploy: `kubectl apply -f deployment_env_selected.yml -n snippet-deployment-configmap-demo`

Get the name of a Pod: `kubectl get pods -l app=my-app -n snippet-deployment-configmap-demo`

```
NAME                             READY   STATUS    RESTARTS   AGE
my-deployment-c5b59bdbf-s8m7h   1/1     Running   0          6s
my-deployment-c5b59bdbf-x826m   1/1     Running   0          6s
```

Check the environment variable inside that Pod (replace the name below with
one from the output above):

`kubectl exec -it pod/my-deployment-c5b59bdbf-s8m7h -n snippet-deployment-configmap-demo -- sh -c 'echo $HELLO'`

Delete: `kubectl delete -f deployment_env_selected.yml -n snippet-deployment-configmap-demo`


## Volume

Mounting the ConfigMap as a volume creates one file per key under the mount
path in every replica's container, with the file content set to the
corresponding value.

Deploy: `kubectl apply -f deployment_volume.yml -n snippet-deployment-configmap-demo`

Get the name of a Pod: `kubectl get pods -l app=my-app -n snippet-deployment-configmap-demo`

```
NAME                             READY   STATUS    RESTARTS   AGE
my-deployment-c5b59bdbf-s8m7h   1/1     Running   0          6s
my-deployment-c5b59bdbf-x826m   1/1     Running   0          6s
```

Check the mounted file inside that Pod (replace the name below with one from
the output above):

`kubectl exec -it pod/my-deployment-c5b59bdbf-s8m7h -n snippet-deployment-configmap-demo -- cat /etc/config/message1`

Delete: `kubectl delete -f deployment_volume.yml -n snippet-deployment-configmap-demo`


## Cleanup

Delete the ConfigMap: `kubectl delete -f configmap.yml -n snippet-deployment-configmap-demo`

Delete the namespace: `kubectl delete namespace snippet-deployment-configmap-demo`
