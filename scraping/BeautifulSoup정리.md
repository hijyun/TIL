_참고 서적 : 라이언 미첼, Web Scraping with Python, 한빛미디어_

# BeautifulSoup 소개
웹 스크레핑은 데이터를 수집하는 작업 전체를 말하며 프로그램을 만들어 웹 서버에 쿼리를 보내 데이터를 요청하고, 이를 파싱하여 필요한 정보를 추출하는 작업을 자동으로 하는는 것이다.
BeautifulSoup라이브러리는 잘못된 HTML을 수정하여 쉽게 탐색할 수 있는 XML 형식의 파이썬 객체로 변환할 수 있다.


```{python}
from urllib.request import urlopen
#BeautifulSoup실행
from bs4 import BeautifulSoup
html = urlopen('https://pythonscraping.com/pages/page1.html')

bs = BeautifulSoup(html.read(),'html.parser')
print(bs.h1)
```
beautifulSoup객체를 만들어 위와 같이 출력하면 페이지에 있는 첫 번째 h1 태그만 반환한다는 사실을 알 수 있다.



```{python}
bs = BeautifulSoup(html.read(),'html.parser')
```
객체를 만들 때 두 가지 매개변수를 넣는다. 첫번째 매개변수는 객체의 근간이 되는 HTML텍스트이고, 두번째 매개변수는 beautifulSoup이 객체를 만들 때 쓰는 구문분석기이다.
html.parser는 파이썬 3과 함꼐 설치된 구문분석기이고 이 외의 널리 쓰이는 구문분석기로 lxml, html5lib 등 이 있다.


* lxml
    * 닫히지 않는 태그, 계층 구조가 잘못된 태그, heads나 body가 없는 등의 문제에서 일일히 멈추지 않고 문제를 수정한다.
    * html.parser에 비해 속도가 조금 더 빠르다.
    * 단점으로 따로 설치해야하며, 서드파티 C언어 라이브러리가 있어야 제대로 동작하므로 사용하기 조금 어렵다.

* html5lib
    * lxml과 마찬가지로 잘못 만들어진 HTML을 수정하고 구문 분석을 시도할 수 있고, 좀 더 다양한 에러를 수정할 수 있다.
    * 외부 프로그램이 있어야 동작할 수 있으므로 html.parser보다 조금 느리다.


## 예외 처리

```{python}
html = urlopen('https://pythonscraping.com/pages/page1.html')
```
위 의 코드에서 생길 수 있는 문제 2가지
1. 페이지를 찾을 수 없거나, URL 해석에서 에러가 생긴 경우

    ex.HTTP 에러. (404,500)
    
2. 서버를 찾을 수 없는 경우

```{python}
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs  = BeautifulSoup(html.read(),'html.parser')
        title = bs.body.h1
    except ArithmeticError as e:
        return None
    return title


title = getTitle('https://pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)
```

위의 코드는 페이지에서 타이틀을 반환하거나, 어떤 문제가 있을 때 None 객첼르 반환하는 getTitle함수를 만든 것이다. None이 반환될 수 있음을 무시하고 None객체에 어떤 함수를 호출하는 경우에 대응하기위해 title이 none인 경우까지 고려하였다.


## find()와 findAll()
find와 findAll을 사용하면 HTML 페이지에서 원하는 태그를 다양한 속성에 따라 쉽게 필터링할 수 있다. 이전엔 bs.tagName을 호출해서 페이지에 처음 나타난 태그를 찾아냈다. bs.findAll을 사용하면 페이지 전체의 태그를 찾을 수 있다. 이름과 속성에 따라 태그를 찾는 것이다.
일단 매개변수를 살펴보자.

|매개변수|내용|
|-------|-----------------------------------|
|tag| 태그 이름인 문자열을 넘기거나, 태그 이름으로 ㅅ이루어진 파이선 리스트를 넘길 수 있다.|
|attributes|속성으로 이루어진 파이썬 딕셔너리를 받고, 그 중 하나에 일치하는 태그를 찾는다.|
|recursive|문서에 얼마나 깊이 찾아들어갈지 결정. True일 경우 findALL함수는 일치하는 태그를 찾아 자식,자식의 자식을 검색. False일 경우 문서의 최상위 태그만 찾는다.|
|text|태그의 속성이 아니라 텍스트 콘텐츠에 일치한다는 것을 찾을때 사용. 일치한는 텍스트 수만큼 넘겨준다.|
|limit|findAll에서만 사용.find는 limit이 1인 것과 같음. 페이지의 항목 처음 몇 개를 찾을지 결정. 페이지에 나타난 순서대로 찾는다.|
|keyword| 특정 속성이 포함된 태그를 선택할 때 사용한다.|

**태그 목록을 .findAll()에 속성 목록으로 넘기면 or 필터처럼 동작한다. 반면,keyword매개변수는 and필터처럼 동작한다.**

* find()
```{python}
find(tag, attributes, recursive, text, keywords)
```
* findAll()
```{python}
find(tag ,attributes ,recursive ,text ,limit ,keywords)
```

예제코드는 다음과 같다.
```{python}
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, "html.parser")
```
```{python}
nameList = bs.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())
```

```{python}
nameList = bs.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())
```


<참고> .get_text()
> .get_text()는 현재 문서에서 모든 태그를 제거하고 유니코드 텍스트만 들어 있는 문자열을 반환한다. 따라서 텍스트 블록 보다는 BeautifulSoup객체에 사용하고, 최종 데이터를 출력,저장,조작 하기 직전에 사용하는 것이 좋다.


## 트리 이동
findAll 처럼 이름과 속성에 따라 태그를 찾는 것이 아닌 문서 안에서 위치를 기준으로 태글르 찾을 때 트리 네비게이션이 필요하다.

### 자식(children)과 자손(descendants)
자식과 자손을 구별해야한다 !

```{python}
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
```
* 자식 : 부모보다 한 태그 아래 있음.
```{python}
for child in bs.find('table',{'id':'giftList'}).children:
    print(child)
```
* 자손 : 조상보다 몇 단계든 아래에 있을 수 있음.
```{python}
for desc in bs.find('table',{'id':'giftList'}).descendants:
    print(desc)
```

일반적으로 BeautifulSoup 함수는 항상 현재 선택된 태그의 자손을 다룬다. 예를들어 bs.body.h1은 body의 자손인 첫 번째 h1 태그를 선택한다. body 바깥에 있는 태그에 대해선 동작하지 않는다. bs.div.findAll('img')도 마찬가지로 첫 번째 div 태그를 찾고, 그 div 태그의 자손인 모든 img 태그 목록을 가져온다.

자식만 찾을 땐 .children을 사용한다.

### 형제 다루기

```{python}
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

for sibling in bs.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sibling) 
```
* next_siblings()

next_siblings() 함수는 이름에서 알 수 있듯이 **다음** 형제만 가져온다.
예를들어 우리가 목록 중간에 있는 임의의 행을 선택하고 next_siblings를 호출했다면 그 다음에 있는 형제들만 반환되는 것이다. 객제는 자기 자신의 형제가 될 수 없기 때문에 자기자신을 건너 뛴다.
위의 코드는 타이틀 행을 선택하고 next_siblings을 호출했기 때문에 그 다음에 있는 형제들만 반환된다.

* previous_siblings()

이 함수는 원하는 형제 태그 목록의 마지막에 있는 태그를 선택할 때 사용한다.

* next_sibling(), previous_sibling() : 하나만 반환한다.

### 부모 다루기
자식이나 형제가 아니라 부모를 찾아야 하는 경우 .parent와 .parents를 사용한다.

```{python}
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')
print(bs.find('img',
              {'src':'../img/gifts/img1.jpg'})
      .parent.previous_sibling.get_text())
```
위의 코드는
1. 이미지를 선택해서
2. 부모 태그를 찾은 후
3. 부모 태그의 마지막 형재를 찾고
4. 그 태그안에 있는 텍스트를 선택한다.

## 기타
* 정규표현식
* 람다표현식
* 속성에 접근하기 