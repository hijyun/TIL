# Static pod
## 스태틱 파드란?

- kube-apiserver를 통하지 않고 kubelet이 직접 실행하는 파드
- kubelet이 직접 관리하고, 이상이 생기면 재시작
    - 지정한 디렉터리에서 yaml파일들을 kubelet이 읽고 파드를 생성하고, 계속 파드가 유지되도록 관리함
    - 파드만 생성할 수 있고, replica나 deployment는 생성 못함
    - kubelet은 오직 pod level에서만 작동
<br>
- kubelet이 실행중인 노드에서만 실행되고 다른 노드에서는 실행되지 않음
- kube-apiserver는 조회는 할 수 있지만 스태틱파드에 어떤 명령을 실행할 수는 없음
    - `kubectl get pods` 명령어로 static pod도 조회 가능
    - kbuelet이 pod를 생성하면 kube-apiserver가 mirror object을 생성함 
    - kube-apiserver를 사용하는 `kubectl edit` or `delete` 명령 사용해서 설정을 바꾸는 것은 불가능
<br>
<br>

## static pod 생성 방법
1. kubelet 설정의 `—pod-manifest-path`라는 옵션에 지정한 디렉터리(`/etc/kubenetes/manifests`)에 스태틱 파드로 실행하려는 파드들을 넣어두면 kubelet 이 감지해서 파드로 실행함
2. 디렉터리를 직접 입력하지 않고 config 옵션으로 staticPodPath를 명시할 수도 있음
    - `-- config=kubeconfig.yaml`로 지정한 다음
    -  `kubeconfig.yaml`에 staticPodPath를 지정
<br>
- staic pod가 생성되면 `docker ps` command로 확인 가능
- kube-apiserver는 HTTP API endpoint로 kubelet에 input을 할 수 있음
<br>
<br>


##  언제 사용? 왜 사용?
- static pod는 kubernetes control planeㅇ[ㅔㅔ 의존적이지 않기 때문에 control plane 자체를 deploy하는 데 사용
<br>
- kube-apiserver나 etcd같은 시스템 파드를 실행하는 용도로 사용
- 즉, 쿠버네티스에서 파드를 실행하려면 kube-apiserver가 필요한데 kube-apiserver자체를 처음 실행하는 별도의 수단으로 스태틱 파드를 이용
- master node에 kubelet을 설치하면 apiserver, controller-manager, etc 등을 위해 docker image를 사용하는 static pod directory에 definition file 생성
<br>
<br>

## Static Pods vs DaemonSets
|Static Pods| DaemonsSets|
|------------------------|-----------------------|
|Created by the Kubelet| Created by Kube-API server(DaemonSet Controller)|
|Deploy Control Palne components as Static Pods| Deploy Monitoring Agents, Logging Agents on nodes|
|Ignored by the Kube-Scheduler|Ignored by the Kube-Scheduler|
