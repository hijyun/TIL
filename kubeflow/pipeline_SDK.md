# [pipeline SDK](https://www.kubeflow.org/docs/components/pipelines/sdk/sdk-overview/)
kubeflow pipeline SDK는 ML 워크플로를 지정하고 실행하는데 사용할 수 있는 python 패키지를 제공한다.

* `kubeflow standalone` 사용

<br>

## install 
python 3.5이상 이 필요. 가이드라인은 python 3.7 사용
<br>
```bash
$ pip install kfp
```
<br>
<br>

---

## Connect to kubeflow Pipelines from outside your cluster

SDK 클라이언트를 사용하여 kubeflow pipelines에 연결하고 환경 변수를 사용해 SDK 클라이언트 구성.
Kubeflow Pipeline standalone은 추가 인증 없이 `ml-pipeline-ui`라는 k8s서비스를 배포함.


<br>

```python
import kfp
client = kfp.Client(host='Input kubeflow pipeline host')
print(client.list_experiments())
```
<br>

아래와 같은 결과가 나오면 정상 적으로 설치된 것.

<br>

```Plain Text
Output exceeds the size limit. Open the full output data in a text editor
{'experiments': [{'created_at': datetime.datetime(2022, 5, 4, 2, 23, 32, tzinfo=tzutc()),
                  'description': 'All runs created without specifying an '
 

 ...

```
<br>
<br>

---
## Build a Pipeline

### library load
```python
import kfp
import kfp.components as comp
```
<br>

### Understanding Pipelines, Pipeline components, Graph

* kubeflow 파이프라인은 컨테이너를 기반으로 ML워크플로의 이식성과 확장성있는 정의를 말한다. 
* 파이프라인의 각 단계는 `ContainerOp`의 인스턴스로 표현되는 구성요소의 인스턴스이다.
* 파이프라인 컴포넌트는 워크플로 한 단계를 수행하는 컨테이너화된 애플리케이션이다.
* 머신러닝의 데이터 수집부터 학습의 과정은 서로 종석성을 가지고있다. 파이프라인 워크플로의 각 단계는 입력과 출력이 다른 단계에 종속될 수 있다. 종속성을 이용해 파이프라인의 워크플로를 그래프로 정의힌다.

<br>




<br>

### Getting started building a pipeline
웹에서 tar를 읽어와서 압축된 tar파일에서 csv를 추출한 뒤 병합하는 코드는 다음과 같이 만들 수 있다.

<br>

#### Build pipeline components
```python
def merge_csv(file_path: comp.InputPath('Tarball'),
              output_csv: comp.OutputPath('CSV')):
  import glob
  import pandas as pd
  import tarfile

  tarfile.open(name=file_path, mode="r|gz").extractall('data')
  df = pd.concat(
      [pd.read_csv(csv_file, header=None) 
       for csv_file in glob.glob('data/*.csv')])
  df.to_csv(output_csv, index=False, header=False)
```

<br>

* import문은 함수 내부에 있어야 한다.</br>
* kfp.components.InputPath 함수의 인수는 kfp.components.OutputPath의 주석이 된다. 이 주석은 Kubeflow pipelines에게 압축된 tar파일을 제공하고 합쳐진 csv파일을 저장할 경로를 생성하려고 알려준다.

<br>

```python
create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file='component.yaml', # This is optional. It saves the component spec for future use.
    base_image='python:3.7',
    packages_to_install=['pandas==1.1.4'])
```

<br>

* kfp.components.create_component_from_func에선 파이프라인 단계를 생성하는 데 사용할 수 있도록 factory함수를 반환하는 데 사용. 
* 이 예제에선 기능을 실행할 기본 컨테이너 이미지, 구성 요소 사양을 저장할 경로, 런티임 시 컨테이너에 설치해야할 PyPl패키지 목록 지정

<br>
<br>

#### Build pipeline

**1**  
kfp.components.load_component_from_url
<br>

```python
web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml')
```

<br>

* kfp.components.load_component_from_url은 파이프라인에서 재사용중인 컴포넌트에 대한 사양을 적은 yaml을 로드하는데 사용


**2**  
파이프라인을 python 함수로 정의

<br>

```python
# Define a pipeline and create a task from a component:
def my_pipeline(url):
  web_downloader_task = web_downloader_op(url=url)
  merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs['data'])
  # The outputs of the merge_csv_task can be referenced using the
  # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']
```
<br>

<정리>

1. 파이프라인 함수의 인수는 파이프라인 매개변수를 정의
2. kfp.components.create_component_from_func및 에 의해 생성된 팩토리 함수
3. kfp.components.load_component_from_url를 사용하여 파이프라인 작업을 생성

<br>
<br>

> web_downloader_task는 url파이프라인 매개변수를 사용하고, merge_csv_task는 web_downloader_task의 data 출력에 사용함.


<br>
<br>

### Compile and run pipeline

#### Option1 : Compile and then upload in UI
* 파이프라인을 컴파일하여 `pipeline.yaml`로 저장
```python
kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')
```

* 저장된 `pipeline.yaml`을 kubeflow Pipeline인터페이스를 사용하여 실행

    * kubeflow에 들어가 `Upload pipeline` > `Upload a file` > 'pipeline.yaml' 올리기  > Create > 파이프라인 생성 > `Create run` 
 
<br>

#### Option2 : run the pipeline using Kubeflow Pipelines SDK client

* kfp.Client class 인스턴스 생성
 
```python
client = kfp.Client() # change arguments accordingly
```

<br>
<br>

* kfp.Client 인스턴스를 사용해 파이프라인 실행
```python

client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={
        'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    })

```

<br>
<br>
<br>

---
## Building Components
Components는 ML워크플로에서 한 단계를 수행하는 코드의 집합이다. Components를 생성하려면 구성 요소의 implementation을 빌드하고 구성 요소의 specification을 정의해야한다.

* 구성 요소의 입력과 출력은 문자열, 숫자, 논리값 같은 작은 값으로 전달됨. csv같이 큰 파일은 경로로 전달해야함.
* 출력을 반환하려면 출력 데이터를 파일로 저장하고 파이프라인에 알려줘야함. 

<br>
<br>

### Containerize Component's code
kubeflow pipeline에서 component를 실행시키려면, component는 반드시 Docker 컨테이너 이미지로 패키지 되어야하고, container registry에 publish되어야함.

<br>

1. base container image Dockerfile 생성

* base container image
* 코드가 돌아가기위해 설치해야할 종석성들
* 컨테이너에 component를 위해 돌아가야할 코드 파일 copy

<br>

```yaml
FROM python:3.7
RUN python3 -m pip install keras
COPY ./src /pipelines/component/src
```

<br>

2. `build_image.sh`라는 이름의 스크립트 생성

* 컨테이너 이미지를 빌드하고 컨테이너 레지스트리에 push하기 위해 Docker사용. 쿠버네티스 클러스터가 component를 실행시키기 위해 컨테이너 레지스트리에 접근할 수 있어야함.
* 아래의 예시는 컨테이너 이미지를 빌드하고, 레지스트리에 push하고 strict image name을 출력하는 예시이다.
각 component를 실행할 때 strict image name을 사용하면 어떤 버전의 컨테이너를 사용하는지 확인할 수 있어서 좋다.



<br>

```sh
#!/bin/bash -e
image_name=gcr.io/my-org/my-image
image_tag=latest
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")" 
docker build -t "${full_image_name}" .
docker push "$full_image_name"

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
```

<br>

* `image_name` : 컨테이너 레지스트리에 있는 컨테이너 이미지 이름을 지정

<br>

```bash
chmod +x build_image.sh
```

3. `build_image.sh` 스크립트 실행
4. `docker run` 

<br>
<br>

### Creating a component specification
component의 implementation, interface, metadata를 정의할 component specification을 생성해야함.

* component’s metadata : name, description
* component’s interface : components의 input, output
* component’s implementation : Docker 컨테이너 이미지. 어떻게 input을 통과해서 output을 얻는지

<br>


#### Define component's implementation

#### Define component's interface

#### Define component's metadata

<br>
<br>


<br>








<br>
<br>



# Reference
* [kubeflow Docs](https://www.kubeflow.org/docs/components/pipelines/sdk/build-pipeline/)

