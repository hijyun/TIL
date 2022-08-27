# Monitor Cluster Components
## Monitor
- 쿠버네티스에서 기본적인 시스템 메트릭인 CPU, Memory 부터 클러스터에 노드 수, 컨테이너 상태 등 많은 것을 모니터링 해야한다.
- 이런 것들을 모니터링하고 metric을 저장하고 분석하기 위한 솔루션이 필요한데 쿠버네티스는 이 모든것들을 제공하지는 않기 때문에 Prometheus, Metrics-Server, ELK, Datadog, Dynatrace같은 오픈소스 솔루션들이 필요하다.

<br>
<br>

## Heapster vs Metric Server
- Heapster는 kubenetes를 모니터링하기 위한 오리지널 프로젝트였지만 현재는 사용되지 않는다.
- Metric server는 쿠버네티스 모니터링 아키텍처에서 core metric pipeline을 효율적으로 사용하려고 heapster대신 도입한 것이다. 

<br>
<br>

## Metic Server
- kubernetes cluster당 하나의 metric server가 있다.
- metric server는 **in memory monitoring solution**
<br>

### metric이 생성되는 과정
- metric server는 kubelet으로 각 노드에 agent를 run하고, metric을 수집해 메모리에 저장한 후 파드나 노드의 메트릭 데이터를 kube-apiserver로 조회하는 Metric API를 제공한다.
- kubelet은 `cAdvisor`나 `Container Advisor`같은 subcomponent을 포함한다.
- `cAdvisor` : 파드로부터 메트릭을 조회하고, kubelet API를 통해 metric server를 위한 메트릭으로 노출시킨다.
- k8s에 필요한 핵심데이터는 etcd에 저장되지만, metric data까지 etcd에 저장하면 부하가 발생할 수 있기 때문에 메모리에 저장한다.
- 단, 메트릭 서버용으로 실행한 파드를 재시작하면 수집했던 데이터를 삭제
- 보관주기를 길게 하려면 별도의 외부 스토리지를 사용해야한다.

<br>
<br>

### Metrics Server - Getting Started
1. minikube 를 사용할 때 
<br>

```
minikube addons enable metrics-server
```

<br>

2. other env
    - git clone 하기
```
git clone https://github.com/kubernetes-incubator/metrics-server.git
```

<br>

```
kubectl create -f deploy/1.8+/
```

<br>
<br>

### node와 pod의 CPU, Memory 사용량 확인하기
metric server가 실행되고 난 뒤 kubectl top command로 사용량을 확인할 수 있다.

```
kubectl top node
```

<br>

![topnode](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F46FWU%2FbtrKLaiQOMq%2FzqqsTPAC3KkAkTKuJFUyMk%2Fimg.png)

```
kubectl top pod
```
<br>
