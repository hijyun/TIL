# bentoML 이란?

```plain Text
BentoML is an open-source platform for building, shipping, and scaling AI applications.


" From trained ML models to production-grade prediction services with just a few lines of code " 
```

</br>
</br>

bentoML은 손쉽게 모델 API를 개발하고 서빙하고 배포할 수 있게 함으로써 엔지니어가 비즈니스에 집중할 수 있도록 돕습니다. 다양한 모델 프레임워크와 함께 작동할 수 있다는 유연성과 더불어, 모델 제작 및 훈련부터 모델 서비스화, API 배포 및 관리에 이르기까지 다양한 단계에서 필요한 기능을 제공하여 최근 생태계를 빠르게 확장해 나가고 있습니다.

</br>

bentoML의 특징을 살펴보면 다음과 같습니다.

- 쉬운 사용성
- Online/Offline Serving 지원
- TF,PyTorch,Keras,XGBoost등 major 프레임워크 지원
- Docker, Kubernetes, AWS, Azure 등 배포 환경 지원 및 가이드 제공
- Flask 대비 100배의 처리량
- 모델 저장소(Yatai) 웹 대시보드 제공
- 데이터 사이언스와 DevOps 사이의 간격을 이어주며 높은 성능의 Serving이 가능하게 함

</br>
</br>

![image](https://github.com/hijyun/TIL/assets/54613024/68a6043f-92eb-40e7-b479-0362a3ca4248)

</br>
</br>

# 개념
 <U>BentoML</U>은 **Bento**, **Runner**, **Yatai**로 구성됩니다.


```Plain Text
* Concept

BentoML로 모델을 서빙하는 과정이란 ... ( ⸝⸝•ᴗ•⸝⸝ )੭⁾⁾

Yatai🏮(일본식 포장마차)에서 Bento🍱(일본 도시락)에 들어갈 음식🍤(model artifact/code)을 Packing🧑🏻‍🍳(모델을 저장-Dockerize)하여, Runner🚚가 배달🍲(Deploy)하는 과정입니다.


🏮 =========> 🚚 >>>>>>>>>>> 🍲
```

</br>
</br>

![image](https://github.com/hijyun/TIL/assets/54613024/21d04150-5464-43ef-8694-a0a263ed9e6a)


 </br>

- Bento: 머신러닝 모델 및 실제 서비스 코드가 포함되어 하나의 Bento로 패킹된 것

    - Bento는 bentoML에서 사용되는 모델과 그와 관련된 모든 코드, 리소스를 패키징하는 단위입니다. Bento 객체는 학습된 모델, 전처리 및 후처리 코드, 필요한 종속성, 설정 파일 등을 포함할 수 있습니다. 이러한 모든 요소는 모델 서비스화와 관련된 기능을 실행하는 데 필요한 모든 것을 포함합니다.

- Runner: 저장된 모델을 계산하여, 실질적인 inference가 수행되는 부분 

    - Runner는 Bento 객체를 실제로 실행하는 역할을 담당합니다. Runner는 Bento 객체를 가져와서 예측을 수행하거나 API 엔드포인트를 생성하는 등의 작업을 수행합니다. bentoML은 다양한 종류의 Runner를 지원하여 다양한 배포 및 실행 환경에 맞게 모델을 실행할 수 있습니다. 예를 들어, CLI 명령어를 통해 로컬 환경에서 실행하거나, RESTful API를 통해 원격으로 실행할 수도 있습니다.

- Yatai: Bento의 배포 및 단위 관리

    - Yatai는 bentoML에서 모델 저장소와 관련된 기능을 담당하는 중앙 관리 서버입니다. Yatai는 Bento 객체를 등록, 버전 관리, 추적 및 관리할 수 있는 저장소를 제공합니다. 또한, 배포 구성 및 관리, 모델 서비스 추적, 협업 기능 등을 지원하여 여러 사용자 및 팀이 모델을 공유하고 관리할 수 있도록 합니다. Yatai를 통해 여러 버전의 모델을 관리하고 원하는 버전을 검색하고 배포할 수 있습니다.


</br>
</br>


# 컴포넌트

-- BentoService : 모델이 어떤 아티팩트 들로 구성되어있는지, 어떤 환경이 필요한지 등을 담고 있는 단위</br>
-- Service Environment </br>
-- Model Artifact</br>
-- Model Artifact Metadata</br>
-- Model Management & Yatai : Yatai(Model Management Component)와 연동 공식 지원. 모델 저장소 역할.</br>
-- API Function and Adapters : predict 함수와 @api 데코레이터를 통해 API 객체를 선언, 최대 Latency 등 상세한 스펙 사항을 정의, 추론 로직 정의</br>
-- Model Serving</br>
-- Labels</br>
-- Retrieving BentoServices</br>
-- WEB UI</br>


</br>
</br>

# 기능
![image](https://github.com/hijyun/TIL/assets/54613024/51e780a4-7378-444c-90f7-f7d1375d821c)
</br>
- MLflow와 연동
- 멀티 모델 기능
- 커스텀 URL 기능
- 커스텀 인풋 전처리와 배치 지원 기능
- 인풋 명세 기능
- 배치 기능
- 패키징 및 Dev 환경 테스트 기능
- 패키지 파일의 구성 및 설명
- 로깅
- 모니터링 기능


</br>
</br>


# 사용 방법

1. 모델 학습
2. BentoService 인스턴스 만들기
3. BentoService으로 학습된 모델 artifact 패키징 (Pack)
4. BentoService으로 Bento에 저장(Save)
5. Docker Image Build(컨테이너화) 
6. Serving 배포 


</br>


<br>
</br>

# reference
- https://engineering.linecorp.com/ko/blog/mlops-bentoml-1
- https://docs.bentoml.com/en/latest/
- https://zzsza.github.io/mlops/2021/04/18/bentoml-basic/
- https://zuminternet.github.io/BentoML/
