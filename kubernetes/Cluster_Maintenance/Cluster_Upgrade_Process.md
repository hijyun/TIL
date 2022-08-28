#  Cluster Upgrade Process

## cluster upgrade
- kubernetes components들이 서로 다른 release version을 가질 수 있는데 나머지 components들은 kube-apiserver release verison 보다 클 수 없다.
    - controller manager, scheduler는 kube-apiserver보다 1 version만 낮을 수 있다.
    - kubelet이랑 kube-proxys는 2 version보다 낮을 수 있다.
    - kubetl은 kube-apiserver보다 한 버전이 높거나 낮을 수 있다.

<br>

- 하위 버전을 지원한다는 특성 때문에 `live upgrases`가 가능하다.
- k8s는 기본적으로 최신버전 - 3 까지만 지원을 해준다.
- upgrades는 one minor version마다 해야한다.

<br>

- upgrades process는 cluster가 어떻게 구성되어있는지에 따라 다르다.
- GKE로 구성했을 경우 쉽게 업그레이드할 수 있고, kubeadm을 사용했을 경우 `kubeadm upgrade paln`과 `kubeadm upgrade apply`를 사용할 수 있고, 그 외의 경우는 다른 방법을 사용한다.

<br>
<br>

- kubeadm 을 사용해 cluster를 구성한 경우
## upgrade step
1. upgrade master node
    - ㅡmaster node가 비활성화 된 동안 control plane에 있는 components들이 비활성화 된다.
    - workder node에 있는 product들의 동작은 영향을 받지 않지만, kubectl 같은 명령어로 접근해서 리소스를 확인하는 작업은 불가능하다.
    - 새로운 application을 deploy하거나 존재하는 app을 삭제하거나 수정하는 것도 불가능하다.
    - controller manager가 동작하지 않기 떄문에 pod가 죽었을 경우 재생성되지 않는다.

<br>

2. upgrase worker node 
    - 방법 1) 한 번에 전부 업그레이드
        - 업그레이드 되는 동안 사용자는 서비스에 접근할 수 없음
    - 방법 2)하나씩 업그레이드
        - 업그레이드 시킬 노드에 있는 파드를 다른 곳으로 옮긴 다음 노드를 업그레이드 시키는 방식으로 진행
    - 방법 3) cluster에 새로운 저번의 노드를 추가 
        - 이 방법은 cloud환경같이 새로운 노드를 쉽게 프로비저닝 할 수 있는 환경에서 편리하다.
        - 새로운 버전의 노드를 추가하고 기존의 파드를 옮긴 다음 이전 버전의 노드를 삭제하는 과정을 반복해 진행한다.

<br>
<br>

## kubeadm - upgrade

<br>

```
kubeadm upgrade plan
```

- cluster, kubeadm, component들의 버전을 알 수 있다.
- cluster 버전 업그레이드가 끝나면 kubelet의 버전도 업그레이드 해야하는데 kubeadm은 kubelet의 버전 업그레이드를 지원하지 않는다. 


<br>

```
apt-get upgrade -y kubeadm=1.12.0-00
```

<br>

```
kubeadm upgrade apply v1.12.0
```

<br>

```
kubectl get nodes
```

- 이때 나오는 버전은 kubelet의 버전임

<br>
- kubelet upgrade
<br>

```
apt-get upgrade -y kubelet=1.12.0-00 
```

<br>
이렇게 하면 master node의 version이 업그레이드 된 것을 확인할 수 있다.

```
systemctl restart kubelet
```

<br>

```
kubectl get nodes
```

<br>

- worker node upgrade
<br>


```
kubectl drain node-1
```

<br>
- drain은 cordon을 포함

<br>

```
apt-get upgrade -y kubeadm=1.12.0-00
apt-get upgrade -y kubelet=1.12.0-00 
kubeadm upgrade node config --kubelet-version v1.12.0
systemctl restart kubelet
```

<br>

```
kubectl uncordon node-1
```

- 이 과정을 모든 worker nodes에 대해서 반복한다.