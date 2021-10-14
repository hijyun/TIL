# Scrapy
웹 크롤링은 페이지의 모든 링크를 찾고, 내부 링크와 외부 링크의 차이를 알아내고, 새 페이지로 이동하는 일을 계속 반복하는 작업이다.
스크레이피를 사용하면 이런 수고를 상당히 덜 수 있다.

## Scrapy 설치 
* pip 설치 관리자로 설치하는 방법
    ```{}
    $ pip install Scrapy 
    ```
* 아나콘다 패키지 관리자로 설치하는 방법
    ```{}
    conda install -c conda-forge scrapy
    ```

## 새 스파이더 초기화
scrapy에서는 각 프로젝트를 하나의 스파이더spider라고 부른다. 

현재 디렉터리에 새 스파이더를 만드는 방법
```{}
scrapy startproject <스파이더 명>
```
이 책에서는 wikiSpider라는 이름을 주었다.
이 명령행을 실행하면 프로젝트 디렉터리에 서브 디렉터리가 생긴다. 이 디렉터리의 파일 구조는 아래와 같다.
![treeWikiSpider](https://user-images.githubusercontent.com/54613024/137235002-1977eb31-d65a-40ab-80fe-4a6159cf25bc.png)


## 간단한 스크레이퍼 작성하기
wikiSpider/wikiSpider/article.py라는 파일을 만들어 아래와 같이 코드를 작성한다.
```
import scrapy

class ArticleSpider(scrapy.Spider):
    name='article'

    def start_requests(self):
        urls = [
            "http://en.wikipedia.org/wiki/Python_%28programming_language%29",
            "https://en.wikipedia.org/wiki/Functional_programming",
            "https://en.wikipedia.org/wiki/Monty_Python"]
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        print('URL is: {}'.format(url))
        print('Title is: {}'.format(title))
```

* 클래스 이름을 이 디렉터리 이름과 다르게 정할 수 있다. 각 유형에 따라 스파이더를 따로 두면서 이들 전체는 하나의 스크레이피 프로젝트에서 실행할 수 있다.

article 스파이더를 실행하는 코드
```python
scrapy runspider article.py
```
