# Volumes

</br>

## 사용하는 이유
- 컨테이너는 기본적으로 stateless앱 컨테이너를 사용.
- 이점은 노드에 장애가 발생해서 컨테이너를 새로 실행 했을 때 다른 노드로 자유롭게 옮길 수 있다는 장점을 갖지만 컨테이너에 저장한 데이터가 사라질 수 있다는 단점이 되기도함.
- 컨테이너를 재시작하더라도 데이터를 유지하기 위해서 ! 

</br>
</br>

## k8s에서 사용할 수 있는 볼륨 플러그인
- 클라우드 서비스에서 제공하는 볼륨 서비스 : awsElasticBlockStore, azureDisk, azureFile ...
- 컨테이너가 실행된 노드의 디스크 : emptyDir, hostPath, local
  - 내부 호스트의 디스크를 사용하는 방식
  - nfs볼륨 플로그인을 이용하면 하나의 컨테이너에 볼륨을 붙여서 NFS 서버로 설정해두고, 다른 컨테이너에서 NFS 서버 컨테이너를 가져다가 사용하도록 설정할 수 있음
- 이외에도 persistentVolumeClaim, configMap, cinder, scaleIO ... 등이 있다 

</br>
</br>

## emptyDir
- 파드가 실행되는 호스트의 디스크를 임시로 컨테이너 볼륨에 할당해서 사용하는 방법
- 임시 디렉터리를 마운트하는 방법
- 파드가 사라지면 emptyDir에서 할당해서 사용했던 볼륨의 데이터도 함께 사라진다.
- 주로 메모리와 디스크를 함께 이용하는 대용량 데이터 계산에 사용됨

<br>

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

</br>
</br>

## hostPath
- 파드가 실행된 호스트의 파일이나 디렉터리를 파드에 마운트한다.
- 호스트에 있는 실제 파일이나 디렉터리를 마운트 한다.
- emptyDir은 단순히 컨테이너를 재시작했을 때 데이터를 보존하는 역할이라면 hostPath는 파드를 재시작했을 때에도 호스트에 데이터가 남는다.
- 호스트의 중요 디렉터리를 컨테이너에 마운트해서 재사용할 수 있음
- `/var/lib/docker` 같은 도커 시스템용 디렉터리를 컨테이너에서 사용할 때나 시스템용 디렉터리를 마운트해서 시스템을 모니터링 하는 용도로 사용한다

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # directory location on host
      path: /data
      # this field is optional
      type: Directory
```


</br>

- (참) 컨테이너 안에 접속해서 `/test-pd` 디렉터리 확인하는 방법
  - `kubectl exec test-pd -it -- sh` , `cd /test-pd`


- `.spec.volumes[].hostpath.type` 필드 값 종류 :  https://kubernetes.io/docs/concepts/storage/volumes/ 

</br>
</br>


## nfs (network file system) 
- 기존에 사용하는 NFS 서버를 이용해서 파드에 마운트 하는 것
- 여러 개 파드에서 볼륨 하나를 공유해 읽기/쓰기를 동시에 할 때도 사용 
- 파드 하나에 안정성이 높은 외부 스토리지를 볼륨으로 설정한 후에 해당 파드에 NFS 서버를 설정한다.
- 다른 파드는 해당 파드의 NFS 서버를 nfs 볼륨으로 마운트한다.
- (여러 개 파드에서 하나의 nfs 볼륨 하나를 공유) 고성능이 필요한 읽기/쓰기 작업이라면 이러한 구성을 사용하기가 어려움. 하지만, 데이터의 안정성을 높인 간단한 파일 공유가 필요하다면 괜찮다.

<br>

- NFS 서버가 있을 때 마운트 하는 방법

```
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /my-nfs-data
      name: test-volume
  volumes:
  - name: test-volume
    nfs:
      server: my-nfs-server.example.com
      path: /my-nfs-volume
      readonly: true

```



</br>
</br>


# 참고
- 쿠버네티스 입문, 동양북스
- https://kubernetes.io/docs/concepts/storage/volumes/
