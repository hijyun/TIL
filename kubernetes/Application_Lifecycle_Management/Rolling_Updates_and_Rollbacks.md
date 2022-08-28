# Rolling Updates and Rollbacks
## Deloyment
### Rollout and Versioning
- Deployment를 생성하면 rollout이 트리거되면서 새로운 버전의 deployment Revision1이 생성된다.
- 이후 컨테이너가 업데이트되면 새로운 rollout이 트리거되면서 새로운 버전의 deployment Revision2가 생성된다.
- 이것은 버전의 변화를 트랙하고, roll back 을 가능하게 한다.

<br>

- Rollout Command
<br>

```
kubectl rollout status deployment/myapp-deployment
```
<br>
<br>
- 히스토리 보기

```
kubectl rollout history deployment/myapp-deployment
```

<br>
<br>

### Deployment Strategy
1.Recreate
- 새로운 버전을 배포할 떄 기존 버전 삭제 -> 새로운 버전 생성하는 전략
- 삭제하고 생성하는 사이에 **Application Down**이 된다.
- defalut x
<br>

2.RollingUpdate
-  **Application Down**이 되지 않아 장점
- default strategy

<br>
- 전략에 따라 `kubectl describe deployment deployment-name`를 했을 때 나오는 결과가 다르다.
<br>

### How to update image of applicaiton
1. kubectl apply 사용하기
    - `deployment-definition.yaml` 수정
    - `kubectl apply -f deployment-definition.yaml`

<br>
2. kubectl set 사용하기

```
kubectl set image deployment/myapp-deployment \ ngix=ngix:1.9.1
```

<br>
<br>

### Rollback

<br>

```
kubectl rollout undo deployment/myapp-deployment
```