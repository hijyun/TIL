# Backup and Restore Methods

## Backup Candidates
- Resource Configuration
- ETCD Cluster
- Persistent Volumes

<br>
<br>

## Backup - Resource Configuration
- Resource Configuration의 경우 declarative 한 방식을 사용하는게 configuration을 저장하기 위해 좋다.
- declarative한 방식을 사용했을 때, 가장 좋은 방식은 yaml을 git에 저장해 버전 관리를 하는 것이다.

<br>
<br>

- declarative 한 방식과 imperative한 방식을 모두 사용할 수 있으므로 resource configuration backup을 위한 최선의 방법은 query the API server이다.

<br>

```
kubectl get all --all-namespaces -o yaml > all-deploy-services.yaml
```

<br>
- 위의 command를 사용하여 Resource configuration을 yaml 형태로 저장할 수 있다.

<br>
<br>

## Backup -ETCD
- ETCD는 cluster의 상태에 대한 정보를 저장한다.
- `etcd.service`에서 `--date-dir=/var/lib/etcd`를 백업해야한다.
- etcd는 **snapshot solution**을 사용할 수 있다. 

<br>

```
ETCDCTL_API=3 etcdctl \
    snapshot save snapshot.db(스냅샷 이름)
```

<br>
<br>

## Restore - ETCD
1. stop kube-apiserver

<br>

```
service kube-apiserver stopped
```

<br>

2. etcdctl 명령어로 특정 snapshot을 restore 한다.

```
ETCDCTL_API=3 etcdctl \
    snapshot restore snapshot.db \
    --data-dir /var/lib/etcd-from-backup
```

<br>

- restore가 실행되면 새로운 etcd 클러스터가 만들어지고, configured된다. 기존의 클러스터와 새로운 클러스터가 결합되지않도록 한다.
- 이 command를 실행하면 새로운 data dir이 생성되고, etcd.service config에도 새로운 data dir을 사용한다.

<br>

그 후 daemon 을 reload하고
<br>

```
systemctl daemon-reload
```

<br>
etcd를 재시작한다.
<br>

```
service etcd restart
```

<br>
이제 kube-apiserver를 시작한다

```
service kube-apiserver start
```

<br>
<br>

- etcd backup을 수행할 때는 option으로 아래의 것들을 명시해주어야한다.

- `--endpoints=`
- `--cacert=`
- `--cert=`
- `--key=`