
# Kubernetes Monitoring Architecture
: 클러스터의 상태와 클러스터 안에 실행 중인 파드들을 모니터링 하는 방법에 대해 알아보자.

- system metrics 
- service metrics
- core metric pipeline
- monitoring pipeline

<br>

## system metrics
- 노드나 컨테이너의 CPU, Memory utilization 같은 시스템 관련 메트릭
</br>
1. core metrics
    - 쿠버네티스 내부 컴포넌트들이 사용하는 메트릭
    - 현재 클러스터 안이나 내장 오토스케일링에서 사용할 수 있는 자원이 얼마인지 파악
    - `kubectl top` command에서 보여주는 cpu/memory 사용량, pod/container의 disk 사용량 등 
</br>
2. non-core metrics
    - k8s가 직접 사용하지 않은 다른 시스템의 메트릭  

<br>
<br>

## service metrics
- application을 모니터링 할 때 필요한 메트릭
</br>
1. k8s 인프라 컨테이너에서 수집하는 메트릭
    - 클러스터를 관리할 때 참고해 사용
</br>
2. 사용자 애플리케이션에서 수집하는 메트릭
- 웹 서버 응답 시간 (response time) 관련 값이나 시간당 HTTP 500 에러가 몇 건이나 나타났는지 등 서비스 관련 정보를 파악
- HPA에서 사요자 정의 메트릭으로 사용할 수 있다.

<br>
<br>

## core metric pipeline
- 쿠버네티스 관련 구성 요소를 직접 관리하는 파이프라인이며 core 요소 모니터링을 담당한다.
- kubelet, metric server, metric api 등으로 구성되어 있다.
- 여기서 제공하는 metric 시스템은 컴포넌트에서 사용한다.
- 주로 스케줄러나 HPA 등에서 작업할 때의 기초 자료로 활용한다.
- 별도의 외부 서드파티 모니터링 시스템과 연계하지 않고 독립적으로 운영된다.

<br>

- kubelet에 내장된 `cAdvisor`는 node/pod/container의 사용량 정보를 수집한다.
- metric server는 이 정보들을 kubelet에서 불러와 메모리에 저장한다.
- 이렇게 저장된 metric 정보는 master의 metric API를 이용해 다른 시스템 컴포넌트가 조회할 수 있다.
- 단, 메모리에 저장해서 저장 용량의 한계가 있어 짧은 기간의 정보만 저장

<br>
<br>

## monitoring pipeline
- 기본 메트릭을 포함한 여러 가지 메트릭을 수집한다.
- 여기서 수집한 메트릭은 쿠버네티스 시스템보다는 클러스터 사용자에게 필요한 모니터링에 사용한다.
- 외부 모니터링 솔루션이 필요한데 모니터링 파이프라인은 시스템 메트릭과 서비스 메트릭을 모두 수집할 수 있다.
- 코어 메트릭 파이프라인과는 분리되어 있다.

<br>
- 많이 사용 히는 조합
    - cAdvisor + heapster + influxDB
    - cAdvisor  + Prometheus

## Structure of kubernetes monitoring architecture
<br>

![monitoring](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fw0cli%2FbtrKHdumdNK%2FjEszjkt0FDWn5oa9KZp1zk%2Fimg.png)