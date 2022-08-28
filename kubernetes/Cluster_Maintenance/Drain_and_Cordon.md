# OS Upgrades
: cluster의 노드를 유지보수(ex. Security path)를 위해 안정적으로 내리려면 어떻게 해야할까?
- node를 내리려고 할 때 5분안에 node를 살리면 pod가 실행되지만 5분이 지나면 pod는 terminated 된다.
- 이것은 kube-controller-manager에서 `--pod-eviction-timeout=5m0s`이 defalut 값이 5분으로 설정되어 있기 때문이다.
- pod eviction time이후 노드가 다시 생성되었을 때 replica set에 있는 pod들은 다른 노드에서 살아나지만, 그렇지 않은 pod들은 복원되지 못한다.
- 만약 노드가 다운되는 시간이 5분 이내일 것으로 예상되면 **quick upgrade**나 **reboot**가 가능하지만, 그렇지 않을 것으로 예상될 경우 사용할 수 있는 안전한 방법은 다음과 같다.
    - drain
    - cordon

<br>
<br>

## kubectl drain
- drain은 노드 관리 등의 이유로 지정된 노드에 있는 파드들을 다른 노드로 이동시키는 명령이다.

<br>

```
kubectl drain node-name
```

<br>

- 먼저 새로운 파드를 노드에 스케줄링해서 실행하지 않도록 설정한다.
- 기존 해당 노드에서 실행중이던 파드들을 삭제한다.

<br>

- 이떄, 노드에 daemon set로 실행한 파드들이 있으면 drain설정을 적용할 수 었다. daemon set로 실행한 파드들은 삭제해도 daemon set가 즉시 재실행 시키기 때문이다.
- `--ignore-daemonsets=true` option을 설정하면 데몬세트로 실행한 파드들을 무시하고 드레인 설정을 적용할 수 있다.

<br>

- controller를 이용하지 않고 실행한 파드들도 드레인 설정을 적용할 수 없다.
- controller가 관리하는 pod들은 삭제되더라도 클러스터 안 다른 노드에 재생성되는데 `--force` option을 설정하면 드레인 설정을 적용해 파드를 강제로 삭제할 수 있다.

<br>
- static pod들은 kubelet이 실행하고, kube-apiserver를 이용해서 실행되지 않았으므로 삭제되지 않는다.

<br>

## kubectl cordon
- cordon 명령은 지정된 노드에 추가로 파드를 스케줄링해서 실행하지 않도록 한다.

<br>

```
kubectl cordon node-name
```

<br>

## uncordon
- uncordon할 경우 cordon 된 상태를 해제시켜준다.

<br>

```
kubectl uncordon node-name
```

<br>
<br>

