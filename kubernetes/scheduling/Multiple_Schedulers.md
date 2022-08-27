# Multiple Schedulers

-   node에 pod를 스케줄링하기 전에 custom condition을 체크하는 자체적인 스케줄링 알고리즘을 만들고 싶을 경우
    1.  default scheduler에 스케줄 프로그램을 deploy하거나
    2.  추가적인 scheduler를 쿠버네티스 클러스터에 추가할 수 있음
-   애플리케이션 마다 다른 스케줄러를 이용할 수 있다. 예를들어, 다른 app은 default를 사용하게하고, 특정 app은 custom scheduler를 사용할 수 있다.
-   pod를 생성할 때 어떤 스케줄러를 사용할지 정의할 수 있다.  
      
    

## Deploy Additional Scheduler

-   kube-scheuler binary를 다운로드 받은 후 옵션과 함께 서비스로 실행한다.
-   additional scheduler를 deploy하려면 kube-scheuler binary를 사용하거나 직접 만들어야한다.
-   `--scheduler-name==default scheduler`를 변경한다. 이 이름을 나중에 pod definition file에 사용한다.  
      
    

## Deploy Scheduler - kubeadm

-   kubeadm은 스케줄러를 pod로 실행한다.
-   definition file 위치 : `/etc/kubernetes/manifests/kube-scheduler.yaml`
-   `command` section에는 스케줄러를 실행하기 위해 관련된 option들이 있다.
    -   `--scheduler-name` : 스케줄러 이름
    -   `--leader-elect=` : 여러 마스터 노드에 같은 스케줄러의 복사본이 여러개 있을 때 오직 하나만 한번에 active될 수 있다. 이때, 여러 scheduler 중 스케줄 활동을 이끌 leader를 고르는데 도움을 준다.
        -   master가 존재하는게 아닐 때는 `false`, 여러 개의 master 존재할 때는 `true`
-   `--lock-object-name` : 여러 개의 master가 존재할 때 leader election을 하는 동안 custom scheduler와 default scheduler를 구분한다.
-   option을 생성하고, `kubectl create command`로 스케줄러 pod를 생성한다.

### Deploy Additional Scheduler - kubeadm

-   custom scheduler를 만들기 위해 `/etc/kubernetes/manifests/kube-scheduler.yaml` 파일을 copy 한다.
-   `command` section에서 `--scheduler-name` option을 수정한다.

  
  

## View Schedulers

```
kubectl get pods --namespace=kube-system
```

만들어진 스케줄러는 kube-system 네임스페이스의 파드로 확인할 수 있다.  
  

## Use Custom Scheduler

-   `pod-definition.yaml`에서 `spec` section에 `schedulerName`으로 스케줄러를 지정할 수 있다.
-   `kubectl create -f pod-deficition.yaml`

## View Events

-   어떤 스케줄러가 선택되었는지 어떻게 볼 수 있을까?  
<br>
```bash 
kubectl get events 
```
<br>

-   현재 네임스페이스에 있는 모든 이벤트 목록을 보여주고, 스케줄된 이벤트(REASON)가 어떤 스케줄러를 사용하고 있는지(SOURCE) 알 수 있다.

## View Scheduler Logs

```
kubectl logs my-custom-scheduler(스케줄러 이름) --name-space=kube-system
```