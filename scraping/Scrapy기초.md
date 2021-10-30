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

* start_requests :  스레이피 웹사이트를 크롤링할 때 사용하는 Request객체를 생성. 프로그램에 대해 스크레이피가 정의하는 진입점.

* parse : 사용자가 정의한 콜백 함수 callback = self.parse 를 사용하여 Request 객체로 전달.



article 스파이더를 실행하는 코드
```python
scrapy runspider article.py
```

## 항목 만들기
items.py에선 수집된 항목을 사용자가 지정한 개체에 저장할 수 있다.

```
import scrapy


class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    lastUpdated = scrapy.Field()

```

Article 클래스를 새로 만들어 각 페이지에서 수집할 필드를 만든다.

```
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articleItems'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback='parse_items', follow=True),
    ]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')
        return article
```



* 항목 출력학기
```
$ scrapy runspider articleItems.py -o article.csv -t csv
$ scrapy runspider articleItems.py -o articles.json -t json
$ scrapy runspider articleItems.py -o articles.xml -t xml
```
각 명령은 articleItems 스파이더를 실행하고 지정된 형식의 출력을 지정된 파일에 쓴다. 이때,지정한 파일이 존재하지 않으몬 새로 생성한다.

## 파이프라인
Scrapy는 단일 스레드 애플리케이션이지만 많은 요청을 비동기적으로 만들어 처리할 수 있어 빠른 스크레이퍼를 만들 수 있다. 
스크레이피의 파이프라인을 사용하면 이전 요청의 데이터 처리가 완료되는 것을 기다리는 것이 아니라 응답을 기다리는 동안 데이터를 처리할 수 있으므로 스크레이퍼 속도를 더 빠르게 할 수 있다. 

> 스파이더는 데이터 수집만 담당하게 하고, 데이터 처리는 파이프라인이 담당하도록 만들기


settings.py에서 아래 부분의 주석처리를 제거한다.
```
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wikiSpider.pipelines.WikispiderPipeline': 300,
#}
```
주석을 해제하면 데이터 처리할 때 wikiSpider.piplines.WikispiderPipeline 클래스를 사용한다. 숫자는 우선순위를 의미한다. 0-1000사이의 정수를 쓸 수 있다.

> settings.py 파일에서 여러 작업이 포함된 파이프라인을 여러 개 선언할 수 있다. Scrapy는 항목 유형에 관계없이 모든 항목을 각 파이프라인에 순서대로 전달한다. 따라서 항목별로 고유한 데이터가있다면 파이프라인에 보내기전에 스파이더에서 처리하는 것이 나을 수 있다. 하지만 시간이 오래 걸린다면 파이프라인으로 이동시켜 시동기적으로 처리해 항목 유형에 대해 검사하는 것이 좋다. 

이제 스파이더 코드를 수정해보자.
```
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articlePipelines'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback='parse_items', follow=True),
    ]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        article['lastUpdated'] = response.css('li#footer-info-lastmod::text').extract_first()
        return article
```

파이프라인 piplines.py 수정하기. 
```
from datetime import datetime
from wikiSpider.items import Article
from string import whitespace

class WikispiderPipeline(object):
    def process_item(self, article, spider):
        article['lastUpdated'] = article['lastUpdated'].replace('This page was last edited on', '')
        article['lastUpdated'] = article['lastUpdated'].strip()
        article['lastUpdated'] = datetime.strptime(article['lastUpdated'], '%d %B %Y, at %H:%M.')
        article['text'] = [line for line in article['text'] if line not in whitespace]
        article['text'] = ''.join(article['text'])
        return article
```

process_item은 모든 파이프라인 클래스에 필수 메서드이다. 스크레이피는 이  메서드를 사용하여 스파이더가 수집한 Items를 비동기적으로 전달한다. 여기서 반환하는 파싱된 Article 객체는 로긍 기록되거나, 선택한 형식으로 저장하면 된다.


## Scrapy logging

Scrapy는 표준적인 로그 수준을 사용한다.
* CRITICAL
* ERROR
* WARNING
* DEBUG
* INFO

settings.py에 
```
LOG_LEVEL = 'ERROR'
```
위와 같은 줄을 추가하면 로그 수준을 조정할 수 있다.

로그를 터미널에 출력하지 않고 별도의 로그 파일을 저장하는 코드
```
$ scrapy crawl articles -s LOG_FILE = wiki.logs
```