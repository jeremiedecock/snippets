# PersistentVolume / PersistentVolumeClaim

Same app and same images as `11_sqlite_volume` (backend `4.0`, frontend
`2.0` — nothing to rebuild: **only the YAML changes**), but the `hostPath`
volume is replaced by proper, node-independent storage.

Kubernetes splits storage in two, so that apps stay portable:

- a **PersistentVolume (PV)** is a piece of actual storage in the cluster (a
  cloud disk, an NFS share, a local directory...). Providing PVs is the
  cluster administrator's problem;
- a **PersistentVolumeClaim (PVC)** is an app's *request* for storage
  ("1 GiB, mounted read-write by one node") — see `pvc.yml`. The app only
  references its claim; it does not know or care what actual storage backs
  it.

In practice PVs are rarely created by hand: a **StorageClass** provisions
them on demand. When the PVC appears, the cluster's default StorageClass
creates a matching PV automatically (`kubectl get storageclass` — minikube,
kind and k3s all ship one; on cloud clusters it creates real network disks).

## The fix, and its price

The database now lives in a PV: it survives Pod restarts *and*
rescheduling on another node, and Kubernetes manages its lifecycle. But look
at `backend.yml`: `replicas: 1` (plus `strategy: Recreate`, so that rolling
updates never run two Pods at once). Two reasons:

- `ReadWriteOnce`, the access mode supported by virtually all storage, means
  the volume can only be mounted by **one node** at a time — three Pods
  spread over three nodes cannot share it (`ReadWriteMany` storage like NFS
  exists but is the exception);
- more fundamentally, SQLite is a *file*, not a server: it is not designed
  for several processes on different machines writing to it.

So consistency was bought by giving up replication: one backend Pod, no
load-balancing, no self-healing while the Pod is rescheduled. The next
example restores both properties the standard way: a real database server.

## Deploy

Edit `your-username`, then:
`kubectl apply -f pvc.yml -f backend.yml -f frontend.yml`

See the claim and the automatically provisioned volume behind it:
`kubectl get pvc,pv`

Use it: `kubectl port-forward service/frontend 8080:80`, open
`http://localhost:8080`, Save a message, Read it — always the same answer
now, whatever the node.

## Check that the data really survives

The PVC has its own lifecycle, independent of the Pods:

```
kubectl delete pod -l app=backend        # the Deployment recreates the Pod...
kubectl delete -f backend.yml            # ...or even delete the whole Deployment,
kubectl apply -f backend.yml             # then recreate it
```

then Read again: the message is still there.

Delete everything:
`kubectl delete -f pvc.yml -f backend.yml -f frontend.yml` — deleting the PVC
deletes the underlying PV and its data (with the usual default StorageClass
setting, `reclaimPolicy: Delete`).
