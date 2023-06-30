# Python Ray
<br>

```python
pip install ray
```
<br>

ray는 python을 병렬 및 분산 처리하기 위한 오픈소스 프로젝트이다. 
<br>

</br>

# Ray 아키텍처
- [ray 아키텍처 백서 문서 2018ver](https://www.usenix.org/system/files/osdi18-moritz.pdf)

- [ray 아키텍처 백서 문서 ver2](https://docs.google.com/document/d/1tBw9A4j62ruI5omIJbMxly-la5w4q_TjyJgJL_jN2fI/preview)

</br>
<br>

### 논문 요약

- ray는 분산 학습, 분산 강화학습, 분산 AutoML(Tune) 등 인공지능에 필요한 컴포턴트들을 추상화 해둔 라이브러리 (특히 강화학습의 요구사항을 만족시키기위해 구현)
- ray는 단일 동적 실행 엔진이 지원하는 작업 병렬 및 Actor 기반 계산을 모두 표현할 수 있는 통합 인터페이스를 구현
- 성능 요구 사항을 충족하기 위해 Ray는 분산 스케줄러와 분산 및 Fault-tolerant 저장소를 사용하여 시스템 제어 상태를 관리
- 본 논문에선 강화학습 어플리케이션을 시뮬레이션, 학습 및 제공할 수 있는 범용 클러스터 컴퓨팅 프레임워크 인 ray를 제안
    - ray는 딥러닝,강화학습의 요구사항을 충족시키기 위해 아래 두 가지를 배포
        - 작업스케줄러
        - 계산 계보 및 데이터 개체의 디렉토리를 유지하는 메타 데이터 저장소
    - 상향식 분산 스케줄링 전략 제안. 제어 상태가 샤딩 된 메타 데이터 저장소에 저장되고 다른 모든 시스템 구성 요소는 상태가 없는 시스템 설계 원칙을 제안

</br>

- ray의 목표
    - 대규모 클러스터에서 높은 활용도
    - 기존 시뮬레이터 및 딥러닝 프레임워크와 원활하게 통합

- ray API
![image](https://github.com/hijyun/TIL/assets/54613024/8227bdf5-96b4-40f8-882a-7e95bd225135)

</br>
</br>

### programing model (구성요소)
Ray 는 dynamic task graph computation model 로 구현되어 있습니다. 이 모델은 크게 `Task` 와 `Actor`라는 2가지 추상화 타입으로 제공됩니다. state 의 유무가 가장 큰 차이를 나타냅니다.

</br>


![image](https://github.com/hijyun/TIL/assets/54613024/bbefebf4-d24a-4d7c-a8b0-163891596bd2)

</br>
</br>

- Task :
    - 호출하는 곳과 다른 프로세스에서 실행되는 함수 또는 클래스.@ray.remote 로 감싸진 함수를 Task라고 한다.(클래스일 경우 Actor)호출자와 비동기적(asynchronously)으로 실행된다.
    - stateless worker의 원격 기능 상의 실행. ray.get()을 사용하여 원격 함수를 호출. 결과를 기다리지 않고 다른 원격 함수에 인수로 전달이 가능.

- Actor :
    - Stateful한 워커 프로세스.클래스에 @ray.remote로 감싸면 Actor class가 되며 이 클래스의 함수 호출은 stateful task(상태 정보를 저장해 다시 호출 가능)가 된다.
    - 상태 저장 계산을 나타냄. 각 액터는 원격으로 호출할 수 있고, 직렬로 실행되는 메서드를 노출한다. 메서드 실행이 원격으로 실행되고 future를 반환한다는 점에서 Task 와 비슷하지만 상태 저장 작업자에서 실행된다는 점에서 다름.
- Task는 세분화된 로드밸런싱을 지원. Task는 input을 저장하는 노드에 예약할 수 있고, 중간 상태를 검사하고 복구할 필요가 없어 오버해드가 낮음. 반면, Actor는 직렬화 되어 수행되므로 훨씬 효율적인 세분화된 업데이트를 제공한다.
- object:
    - Task를 통해 반환되거나 ray.put()을 통해 생성되는 값. 데이터의 크기가 큰 경우 ray.put()을 통해 Object로 만들어 Ray에서 빠르게 사용할 수 있다.


</br>
</br>

## Architecture

ray 아키텍처는 

1. API를 구현하는 애플리케이션 계층과
2. 시스템 계층으로 구성됨

</br>

### Application Layer

- Driver : 사용자 프로그램을 실행하는 프로세스
- Worker : 드라이버 또는 호출한 task를 실행하는 상태 비 저장 프로세스. 원격 함수가 선언되면 모든 함수가 작업자에게 작업이 자동으로 할당됨
- Actor : 호출 될 때 노출 된 메서드만 실행하는 상태 저장 프로세스. 이전 메서드 실행으로 인한 상태에 의존한다는 점을 제외하면 메서드를 직렬로 실행

![image](https://github.com/hijyun/TIL/assets/54613024/d355dd1f-7587-4312-93c3-362396a7e78d)


</br>

→ raylet이 각 노드에 할당된 리소스들을 관리

</br>
</br>

### System Layer

- Global Control Store, GCS
    - a server that manages cluster-level metadata, such as the locations of actors, stored as key-value pair
    - 초당 수백만개의 작업을 동적으로 생성할 수 있는 시스템

![image](https://github.com/hijyun/TIL/assets/54613024/0cdc26bf-4b24-42d6-9003-dd50606729f8)

</br>
</br>

- Bottom-up 분산 스케줄러 
![image](https://github.com/hijyun/TIL/assets/54613024/2563a69d-cf2b-4bfd-9b74-34c85f9c009a)

- 글로벌 스케줄러와 로컬 스케줄로를 두어 계층적 스케줄러를 사용
- 글로벌 스케줄러의 과부하를 방지하기 위해 노드에서 생성된 작업은 먼저 노드의 로컬 스케줄러에 저장
- 로컬 스케줄러가 작업을 결정하지 않으면 글로벌 스케줄러로 전달하기 때문에 상향식 스케줄러라고도 함.

</br>
</br>

- In-Memory Distributed Object Store
    - 작업 대기시간을 최소화하기 위해 모든 작업의 입력 및 출력 등을 저장하는 인메모리 분산 스토리지 시스템을 구현
    - 각 노드에서 공유 메모리를 통해 객체 저장소를 구현

</br>
</br>


### Putting Everything Together
![image](https://github.com/hijyun/TIL/assets/54613024/0f67b5de-fcf2-4b38-a2ad-bdb349d411dd)
**0단계)** 원격 함수 add()는 ray init을 할 때 GCS 자동으로 등록되고, 시스템의 모든 작업자에게 배포됨

**1-2 단계)** a와 b가 노드 N1과 N2에 저장. 드라이버는 add(a,b)를 로컬 스케줄러에 제출하여 글로벌 스케줄로로 전달

**3-4단계)** 글로벌 스케줄러는 add(a,b)의 인수 위치를 조회. GCS에서 인수 b를 저장하는 노드 N2에서 작업을 예약하기로 결정.

**5-6단계)** 노드 N2의 로컬 스케줄러는 로컬 객체 저장소에 add(a, b)의 인수가 포함되어 있는지 확인합니다. local store에 객체 a가 없으므로 GCS에서 a의 위치를 조회

**7단계)** a가 N1에 저장되어있음을 알게되면 N2의 객체저장소가 이걸 로컬 저장소로 복제

**8-9단계)** 이제 add()의 모든 인수가 로컬 저장소에 저장되므로 로컬 스케줄러는 공유 메모리를 통해 인수에 액세스하는 로컬 작업자에서 add()를 호출

</br>

- ray.get()이 호출되었을 때 트리거되는 단계별 작업
![image](https://github.com/hijyun/TIL/assets/54613024/9e8ce14d-d1a1-4519-855d-57e4fd84a3cb)
