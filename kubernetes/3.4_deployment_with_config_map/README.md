C.f. https://kubernetes.io/docs/concepts/configuration/configmap/

# Common

`kubectl apply -f configmap.yml`


# Env (all)

`kubectl apply -f deployment_env_all.yml`

Get the name of a pod: `kubectl get all`

```
NAME                        READY   STATUS    RESTARTS   AGE
pod/hello-c5b59bdbf-s8m7h   1/1     Running   0          6s
pod/hello-c5b59bdbf-x826m   1/1     Running   0          6s
...
```

`kubectl exec -it pod/hello-c5b59bdbf-s8m7h -- sh -c 'echo $message1'`

`kubectl exec -it pod/hello-c5b59bdbf-s8m7h -- sh -c 'echo $message2'`

`kubectl delete -f deployment_env_all.yml`


# Env (selected)

`kubectl apply -f deployment_env_selected.yml`

Get the name of a pod: `kubectl get all`

```
NAME                        READY   STATUS    RESTARTS   AGE
pod/hello-c5b59bdbf-s8m7h   1/1     Running   0          6s
pod/hello-c5b59bdbf-x826m   1/1     Running   0          6s
...
```

`kubectl exec -it pod/hello-c5b59bdbf-s8m7h -- sh -c 'echo $HELLO'`

`kubectl delete -f deployment_env_selected.yml`


# Volume

`kubectl apply -f deployment_volume.yml`

Get the name of a pod: `kubectl get all`

```
NAME                        READY   STATUS    RESTARTS   AGE
pod/hello-c5b59bdbf-s8m7h   1/1     Running   0          6s
pod/hello-c5b59bdbf-x826m   1/1     Running   0          6s
...
```

`kubectl exec -it pod/hello-c5b59bdbf-s8m7h -- cat /etc/config/message1`

`kubectl delete -f deployment_volume.yml`

# Cleanup

`kubectl delete -f configmap.yml`