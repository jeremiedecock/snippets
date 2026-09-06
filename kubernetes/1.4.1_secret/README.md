C.f. https://kubernetes.io/docs/concepts/configuration/secret/

# Common

`kubectl apply -f secret.yml`


# Env (all)

`kubectl apply -f pod_env_all.yml`

`kubectl exec -it pod/hello -- sh -c 'echo $message1'`

`kubectl exec -it pod/hello -- sh -c 'echo $message2'`

`kubectl delete -f pod_env_all.yml`


# Env (selected)

`kubectl apply -f pod_env_selected.yml`

`kubectl exec -it pod/hello -- sh -c 'echo $HELLO'`

`kubectl delete -f pod_env_selected.yml`


# Volume

`kubectl apply -f pod_volume.yml`

`kubectl exec -it pod/hello -- cat /etc/config/message1`

`kubectl delete -f pod_volume.yml`


# Cleanup

`kubectl delete -f secret.yml`