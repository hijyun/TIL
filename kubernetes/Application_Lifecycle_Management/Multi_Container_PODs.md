# Multi Container PODs
- WEB Server와 LOG Agent를 함께 동작시켜야한다든지 여러개의 컨테이너를 한번에 실행시켜야하는 경우 Multi-Container Pods를 사용할 수 있다.

<br>
<br>

# Multi-Container PODs Design Pattern
- 파드로 여러 개의 컨테이너를 묶어서 구성하고 실행할 때 몇가지 패턴을 적용할 수 있다.

<br>

![Pattern](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FBXqLJ%2FbtrKHbXzcGG%2FXLAm5r87u4lgzALs7KPpK1%2Fimg.png)

<br>

## Sidecar pattern
- 원래 사용하려던 기본 컨테이너의 기능을 확장하거나 강화하는 용도로 컨테이너를 추가하는 것
- 기본 컨테이너는 원래 목적의 기능에만 충실하도록 구성하고, 나머지 공통 부가 기능들은 사이드카 컨테이너를 추가해서 사용
- ex. 웹서버 컨테이너 - 로그 수집 컨테이너(사이드카 역할) 로 설정하면 웹 서버 컨테이너를 다른 역할을 하는 컨테이너로 변경했을 때 로그 수집 컨테이너는 그대로 사용할 수 있어 재사용성을 높일 수 있음.

<br>
<br>

## Ambassador pattern
- 프록시 역할을 하는 컨테이너를 추가하는 패턴
- 파드 안에서 외부 서버에 접근할 때 내부 프록시에 접근하도록 설정하고 실제 외부와 연결은 프록시에서 알아서 처리 


<br>
<br>

## Adapter pattern
- 어댑터 패턴은 파드 외부로 노출되는 정보를 표준화하는 어댑터 컨테이너를 사용한다는 뜻이다.
- 주로 어댑터 컨테이너로 파드의 모니터링 지표를 표준화한 형식으로 노출시키고 외부의 모니터링 시스템에서 해당 데이터를 주기적으로 가져가서 모니터링 하는데 이용한다.
- 프로메테우스에서 사용