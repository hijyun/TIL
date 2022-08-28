# Application Commands & Arguments

- docker image의 entrypoint의 argument는 `spec.containers.args`에 명시해준다. 
- `spec.containers.args`는 Docker file의 CMD opiton을 overrride한다.
- Docker file의 ENTRYPOINT를 override하기 위해서는 `spec.containers.commad`를 사용한다.

<br>
<br>

# Configure Environment Variables in Applications
- 환경 변수를 설정하기 위해 `pod-definition.yaml`에서 `spec.container.env` property를 사용한다.

- 예시
<br>

```yaml
apiVersion : v1
kind : Pod
metadata : 
    name : simple-webapp-color
sepc:
    containers : 
    - name : simple-webapp-color
      image : simple-webapp-color
      ports:
          - containerPort: 8080
      env :
          - name : App_COLOR
            value : pink

```

<br>

- 이때, EnV Value Type은 3가지가 있다.

<br>

- 1.Plain Key Value
```yaml
    env :
        - name : App_COLOR
            value : pink

```
<br>

- 2.ConfigMap
```yaml
    env :
        - name : App_COLOR
            valueForm :
                configMapKeyRef : 
```

<br>

- 3.Secrets
```yaml
    env :
        - name : App_COLOR
            valueForm :
                secretK : 
```


<br>
<br>

# Configuring ConfigMaps in Applications
## Configmap이란 ? 
- configmap은 key-vlaue 쌍으로 config data를 저장한다.
- 1.Create ConfigMap
- 2. Inject to Pod


<br>

## 왜 필요할까?
- configmap은 컨테이너에 필요한 환경 설정을 컨테이너와 분리해서 제공하는 기능을 제공한다.
- 다른 설정으로 같은 컨테이너를 실행해야 할 때 컨피그 맵을 사용할 수 있다.
- 예를들어, 개발용 상용 서비스에서 같은 컨테이너지만 다른 설정이 필요한 경우
- 컨피그맵을 컨테이너와 분리하면 컨테이너 하나를 여러 용도로 사용할 수 있다.

<br>

## Create ConfigMaps
1. imperative way
    - `--from-literal` : command 자체에서 key value 쌍을 적을떄 사용
    - `--from-file` :  data가 저장된 file 경로를 전달할 때 사용

<br>

```
kubectl create configamp \
    <config-name> --from-literal=<key>=<value> \
                  --from-literal=<key>=<value>
```

<br>

```
kubectl create configamp \
    <config-name> --from-file=<path-to-file> 
```

<br>

2. declarative way

<br>

```
kubectl create -f config-map.yaml
```
<br>

config-map.yaml

```yaml
apiVersion : v1
kind : ConfigMap
metadata :
    name : app-config
data : 
    APP_COLOR : blue
    APP_Mode :prod
```

<br>
<br>

## View ConfigMaps

<br>

```
kubectl get configmaps
```

<br>

```
kubectl describe configmaps
```

## ConfigMap in Pods
1. EnvFrom
    - `pod-definition.yaml`에서 `spec.containers.envFrom.configMapRef`에 configmap `name` 을 명시해준다
2. Single Env
    - `pod-definition.yaml`에서 `spec.containers.envFrom.configMapRef`에 configmap `name` 다음 `key`를 명시해 특정 환경변수만 config할 수 있다.
3. Volume
    - 볼륨 형식으로 컨피그맵을 설정해서 파일로 컨테이너에 제공할수도 있다.
    - `volumes.name.configMap.name` 에 config 이름을 명시한다.

<br>
<br>

# Configure Secrests in Application
## Secret 이란? 
- 시크릿은 비밀번호, OAuth 토큰, SSH 키 같은 민감한 정보들을 저장하는 용도로 사용한다.
- 이런 정보들은 컨테이너 안에 저장하지 않고 별도로 보관했다가 실제 파드를 실행할 때의 템플릿으로 컨테이너에 제공한다.

- 1. Create Secret
- 2. Inject into Pod

<br>
<br>

### Create Secrets
1. imperative way
    - `--from-literal` : command 자체에서 key value 쌍을 적을떄 사용
    - `--from-file` :  data가 저장된 file 경로를 전달할 때 사용

<br>

```
kubectl create secret generic \
    <secret-name> --from-literal=<key>=<value> \
                  --from-literal=<key>=<value>
```

<br>

```
kubectl create configamp \
    <secret-name> --from-file=<path-to-file> 
```

<br>

2. declarative way

<br>

```
kubectl create -f secret-data.yaml
```
<br>

secret-data.yaml

```yaml
apiVersion : v1
kind : Secret
metadata :
    name : app-secret
data : 
    DB_HOST : mysql
    DB_USER : root
    DB_Password : paswrd
```

<br>
- 이때 Secret값은 해시값으로 바꿔주는게 좋다.

- hash값으로 encode 

<br>

```
echo -n 'root' | base64
```

<br>


- hash 값 decode 
```
echo -n 'root' | base64 --decode
```

<br>
<br>

## View Secrets

<br>

```
kubectl get secrets
```

<br>

```
kubectl describe secrets
```

<br>
<br>

## secrets in Pods
1. EnvFrom
    - `pod-definition.yaml`에서 `spec.containers.envFrom.secretRef`에 configmap `name` 을 명시해준다
2. Single Env
    - `pod-definition.yaml`에서 `spec.containers.envFrom.secretRef`에 configmap `name` 다음 `key`를 명시해 특정 환경변수만 config할 수 있다.
3. Volume
    - 볼륨 형식으로 컨피그맵을 설정해서 파일로 컨테이너에 제공할수도 있다.
    - `volumes.name.secret.name` 에 config 이름을 명시한다.

<br>
<br>


