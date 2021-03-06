# 라우팅 개요
* **라우팅**

    : 패킷을 전송하기 위해 송신측에서 목적지까지의 경로를 정하고 정해진 경로(패킷 교환 방식 중 가상 회선 방식)를 따라 패킷을전달하는 일련의 과정
    - 최단 경로, 최소 비용
    - OSI 7 Layers 중 3계층은 IP정보로 통제하는 곳이고, 네트워크 층에서 관리를 한다. 3계층의 대표적인 장비로는 Router가 있고, 라우터는 경로를 설정한다. 3계층의 데이터를 패킷(패킷 통신, 패킷 교환), 데이터그램으로 부른다.
    - 교환망 1. 회선 교환망 2. 패킷 교환망 3. 메시지 교환망
    - 패킷 교환(패킷 통신)은 경로가 지정되어있지 않은 데이터 그램 형태와 가상의 경로가 지정되어 있는 가상 회선 방식으로 나누어진다. 

* 라우팅 알고리즘

    - 최적의 경로를 찾는 방법
        : 최단 경로를 찾는 기준 - ip와 라우터에 대한 정보들 
        - 테이블 -> IP(비용)
        : 알고리즘을 통해 테이블을 갱신(약 30초 간격)하고,테이블의 정보를 갱신하는 알고리즘은 두가지 정도가 있다. (1)거리벡터-RIP (2) 링크상태-OSPF
        - 최단 경료 알고리즘은 Dijkstra 알고리즘이 있다.
    1. 정적 라우팅 알고리즘
        - 관리자가 직접 라우팅 테이블을 설정
    2. 동적 라이퉁 알고리즘
        - 라우팅 정보 변화에 능동적으로 대처

* 라우팅 프로토콜

    |분류방법|구분|내용|
    |---------|------|----------------------------|
    |라우팅 경로 고정| static routing protocol| 수동식, 라우터 부하 경감, 고속 라우팅| 
    |            | dynamic routing protocol| 라우터가 스스로 라우팅 경로를 동적으로 결정. RIP, IGRP, OSFP, EIGRP | 
    |내/외부 라우팅| Interior Gateway protocol| 같은 관리자 하에 있는 라우터 집합내에서 라우팅을 담당하는 라우팅 프로토콜. RIP, IGRP, EIGRP, OSPF |
    ||Exterior Gateway protocol| 서로 다른 라우터 집합 사이에서 사용되는 라우팅 프로토콜. BGP, EGP|
    |라우팅 테이블 관리|Distance Vector|라우팅 테이블에 목적지 까지 가는데 필요한 거리와 방향만을 기록.RIP, IGRP|
    ||Link State Algorithm|라우터가 목적지까지 가는 경로를 SPF(Shortest-Path-First)알고리즘을 통해 모든 정보를 라우팅 테이블에 기록. OSPF|


* AS (Autonomous System)

    : 하나의 관리 도메인에 속해있는 라우터들의 집합
    - IGP (Interior Gateway Protocol)
    - EGP (Extrior Gateway Protocol)

* 라우팅 기본 원칙

: 라우터는 다른 네트워크의 경로를 나타내는 네트워크 IP 주소와 지역 네트워크에 대한 호스트 IP주소를 나열하고 있는 라우팅 테이블을 가지고 있음

* CIDR (Classless Inter-Domain Routing)

: CIDR은 인터넷 라우팅 테이블 크기가 폭증하는 것을 막는 하나의 방법

# RIP (Routing Information Protocol)
* 거래 벡터 알고리즘을 사용
* 가장 단순한 라우팅 프로토콜
* 라우터는 주기적(약 30초 간격)으로 이웃 라우터와 라우팅 정보를 교환
<img width="879" alt="스크린샷 2021-12-02 오후 2 36 47" src="https://user-images.githubusercontent.com/54613024/144364027-48cb6d0b-349c-46fc-add4-c94f9eff216d.png">

## 거리 벡터 알고리즘
: 자신의 라우팅 테이블을 주기적으로 이웃 라이터에게 전송. 이웃 라우터로부터 라우팅 정보를 수신하여 자신의 라우팅 테이블을 갱신하고 이를 통하여 경로를 선택.


* 라우팅 테이블 생성
* 라우터의 초기 라우팅 테이블은 자신의 이웃 정보로 구성
* 각 라우터는 자신의 라우팅 테이블을 모든 이웃 라우터와 교환
* 라우팅 테이블 교환 과정을 반복하여 각 라우터는 전체 네트워크의 정보를 얻음
* 라우팅 테이블 갱신
  <img width="762" alt="스크린샷 2021-12-02 오후 2 44 18" src="https://user-images.githubusercontent.com/54613024/144364801-c22c0c30-78bc-40c7-8057-5b5bb0679f14.png">

  <img width="747" alt="스크린샷 2021-12-02 오후 2 45 17" src="https://user-images.githubusercontent.com/54613024/144364886-2706e093-401f-4f7c-904c-14c0718943bf.png">

## RIP 프로토콜 
* 개요
    - 거리벡터알고리즘을 사용하는 대표적인 라우팅 프로토콜
    - 거리벡터 값으로 홉 카운트 사용
    - RIP 패킷의 대부분은 네트워크 주소와 비용의 쌍인 정보

* 메시지
    - 요청과 응답의 2가지 종류의 패킷 메시지
    - 요청패킷
        - 라우터가 처음 부팅되었을 때 전송
        - 특정목적지정보가타임아웃되었을때전송
    - 응답패킷
        - 매 30초마다 주기적으로 이웃 라우터에게 전송
        - 트리거갱신시자신의라우팅테이블에변화가생겼을때전송
    - 타임아웃 시간동안 라우팅 정보의 수신이 이루어지지 않을 때 
        - 의미 없는 목적지로 간주
        - 일정시간 후 라우팅 테이블에서 삭제
* 문제점
    - 네트워크 규모가 제한.
    - 홉수 제한에 따라 가장 빠른 경로를 선택할 수 없음
    - 라우팅 정보가 30초마다 교환되므로 장애시 전체 네트워크 복구시 많은 시간이 수요 
    - 특정 경로에 루프 가능성
* 해결방안
    - 트리거 갱신: 변경시 즉시 통보함으로써 복구 시간을 줄임
    - Hold down: 무한대인 경로에 대해서 전체 네트워크의 경로가 새로 갱신될 때까지 일정 시간 동안 기다림
    - Split horizon: 라우팅 정보를 전달해준 인터페이스로 재 전송하지 않음으로 루프 방지
    - Route poison: 회선이 고장난 경우 즉시 홉을 16으로 지정하여 전체 네트워크에 전송


# OSPF (Open Shortest Path First)
* 개요
 
    - 링크 상태 알고리즘
    - 네트워크 환경 변화 시 갱신
    - 링크에 대한 비용 시정
    - OSPF 네트워크 모델

## 링크 상태 알고리즘 (Link State Algorithm)
- 라우터는 이웃에 대한 연결정보를 다른 모든 라우터에 전달
- 네트워크 전체 토폴로지에 대한 정보를 얻고 이를 바탕으로 최적의 경로 선택

* 플러딩 (Flooding)
: 링크상태프로토콜을사용하고있는모든라우터에링크상태정보를전송과정
    * 랑크 상태 패킷(LSP: Link State Packet)
        : <img width="721" alt="스크린샷 2021-12-02 오후 4 41 57" src="https://user-images.githubusercontent.com/54613024/144378782-b85bcfbb-7cf0-4b45-9092-449ae0a91592.png">
    * 링크 상태 데이터베이스(Link State Database)
        - 모든 라우터는 동일한 네트워크 맵정보를 보유하며 이것으로 최적의 경로를 계산
        - 공통의 데이터 베이스 유지
    * 최단 거리 트리 – Dijkstra 알고리즘
        - 라우터는 자신을 루트로 하여 목적지까지의 최단 거리 트리 구성
        
        <img width="375" alt="스크린샷 2021-12-02 오후 4 44 40" src="https://user-images.githubusercontent.com/54613024/144379119-6837a2b8-93ac-49cf-b08f-372e7e5c9eab.png">
        
        하나의 노드를 루트로 하여 아크에 연결된 노드를 임시 노드에 두고 최소 비용을 가지는 노드를 찾는 검사를 수행하여 최단거리 트리의 영구 노드를 결정
        1. 트리의 루트가 될 하나의 노드를 정한다.
        2. 1의 노드를 영구노드로 결정한다.
        3. 가장최근에영구노드가된노드의이웃노드를검사한다.
        4. 각 노드에 누적합의 비용을 계산하고 임시 노드로 만든다
        5. 임시 노드들에 대해서 가장 비용이 적은 노드를 찾아 영구 노드로 만든다. 하나이상의 경로가 존재 할 때는 누적합이 가장 작은 경로를 선택한다.
        6. 3.에서 5.의 과정을 모든 노드가 영구노드가 될 때까지 반복한다.

## OSPF (Open Shortest Path First)

- 1980년대 중반 IETF(Internet Engineering Task Force)가 개발
- 링크 상태 알고리즘을 사용
- 모든 라우터는 동일한 토폴로지 데이터베이스 유지, 자신을 중심으로 최적의 경로를 계산
- 네트워크에 변화시 플러딩과정을 통해 갱신
- 수렴시간을 감소
- 라우팅 트래픽 양 감소
- 동작
    - 플러딩을 위해 D class IP 주소를 사용 멀티캐스팅 수행
    - “hello”메시지
        - 이웃라우터에게 자신이 살아있다는 것을 알리기 위해 사용
        - 일정기간동안 “hello”메시지가 없을 때에는 이상상태가 발생했음을 감지하고 그 사실을 플러딩


# BGP (Border Gateway Protocol)
- AS 사이에서 라우팅 정보를 전달
    - 초기에는 전체 라우팅 테이블을 교환, 이후에는 변경된 라우팅 테이블만을 교환
    - 목적지에 대한 모든 경로를 보유
    - 갱신 메시지에는 최적의 경로만을 전송
- TCP로 동작
- AS의 일련번호를 전송
    - AS의 그래프를 생성, 루프 방지
* 경로 설정
    - TCP well-known 포트 179를 사용하여 이웃 노드간의 연결을 유지, 갱신 정보를 교환
    - Keep-alive 메시지를 주기적으로 교환하여 상대방의 동작 유무에 대한 정보를 얻음
* 연결
    * IBGP (Internal BGP)
    : 동일한AS에속한BGP라우터간에동작
    - EBGP (External BGP)
    : 서로 다른 AS에 동작하는 BGP 프로토콜
* 동작 과정
    : AS 12가 AS 9로 전송할 때 (AS4, AS1, AS3)의 경로에 통해 도달할 수 있음을 통지
    <img width="540" alt="스크린샷 2021-12-02 오후 5 48 57" src="https://user-images.githubusercontent.com/54613024/144388514-decaab12-fd44-4275-9346-4014013ab362.png">
 * 메시지 
  : TCP의 연결을 이용하여 신뢰성 있는 라우팅 메시지 전송

    <메시지 종류>
    1. OPEN
        - 다른 라우터와 이웃 관계를 설정시 사용
        - TCP 연결이 성립되면 관련 파라미터의 협상을 위해 보냄
        - OPEN을 거절
            - 식별자를통해중복된연결발견시나버전이서로다른경우
            - NOTIFICATION 메시지에 원인을 알리고 연결 종류
        - 연결 설정시
            -KEEPALIVE 메시지 전송하여 연결 설정을 알림
    2. UPDATE
        - 경로 변동시 전송
        - 새로운경로가더짧은경우에라우팅테이블의값대체,이웃BGP라우터로해당갱신정보전송 

    3. KEEPALIVE
        - OPEN 메시지에 대한 수신 확인 메시지
        - 이웃이 살아 있는지 알기 위해 주기적으로
    4. NOTIFICATION
        - 오류가 발생하였을 경우
        - 송신자가 BGP 세션을 종료하고자 할 경우

# 정리

<img width="710" alt="스크린샷 2021-12-02 오후 6 05 37" src="https://user-images.githubusercontent.com/54613024/144391114-64205bdd-4353-4cc8-a406-ffce6f2eb3c7.png">

![image](https://user-images.githubusercontent.com/54613024/144391247-a3284105-e76c-40e0-870a-d59b28b31c0b.png)


# reference
- 컴퓨터 네트워크 - 개정3판, 정진욱 외 지음, 2018, 생능
