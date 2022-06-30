# Top hits aggregation
`top_hits` aggregator는 집계된 다큐먼트 중 가장 관련있는 문서를 추적한다. 주로 녀ㅠ aggregator로 사용되고, 각 버킷별로 가장 일치하는 문서가 집계된다.

- `top_hits`는 하위 집계로만 사용하는 것이 좋으며 상위 집계로 사용하고 싶은 경우 `collapse`매개변수를 사용하는 것이 더 좋다.

<br>
<br>


## options
- `from` : 가져오려는 첫 번째 결과의 오프셋
- `size` : 버킷당 반환할 크기. 기본값 3
- `sort` : 가장 많이 일치하는 조회수 정렬 방법

<br>
<br>

## example query

```json
{
                    "size": 0,
                    "sort": [
                        {
                            "@timestamp":
                                {
                                    "order": "asc"
                                }
                        }
                    ],
                    "aggs": {
                        "per_min": {
                            "date_histogram": {
                                "field": "@timestamp",
                                "interval": "5m"
                            },
                            "aggs": {
                                "top_hits_test": {
                                    "top_hits": {
                                        "_source": {
                                            "includes": ["@version", "agent.type", "cloud.availability_zone",
                                                         "cloud.instance.id", "cloud.instance.name",
                                                         "cloud.machine.type", "cloud.provider", "datetime",
                                                         "event.dataset", "event.duration", "event.module",
                                                         "host.hostname", "host.id",
                                                         "metricset.name", "metricset.period", "service.type"]
                                        },
                                        "size": 1
                                    }
                                }
                        

                            }
                        }
                    },
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "host.hostname.keyword": {
                                            "value": "bigdata-elasticsearch-data-1"
                                        }
                                    }
                                },
                                {
                                    "range": {
                                        "@timestamp": {

                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
```

<br>
<br>


### result
```json
{
  "took" : 1162,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "per_min" : {
      "buckets" : [
        {
          "key_as_string" : "2022-02-14T06:35:00.000Z",
          "key" : 1644820500000,
          "doc_count" : 3,
          "top_hits_test" : {
            "hits" : {
              "total" : {
                "value" : 3,
                "relation" : "eq"
              },
              "max_score" : 5.363982,
              "hits" : [
                {
                  "_index" : "sym-metric-cpu-2022.02.16-000001",
                  "_type" : "_doc",
                  "_id" : "Sr0VAX8BByga_0qv_prh",
                  "_score" : 5.363982,
                  "_source" : {
                    "cloud" : {
                      "availability_zone" : "nova",
                      "instance" : {
                        "name" : "bigdata-elasticsearch-data-1.novalocal",
                        "id" : "i-000000ea"
                      },
                      "provider" : "openstack",
                      "machine" : {
                        "type" : "k8s.large"
                      }
                    },
                    "agent" : {
                      "type" : "metricbeat"
                    },
                    "datetime" : "2022-02-14T06:36:40.000Z",
                    "service" : {
                      "type" : "system"
                    },
                    "@version" : "1",
                    "host" : {
                      "hostname" : "bigdata-elasticsearch-data-1",
                      "id" : "7445e51dbde9149b759b77ee5ab144c3"
                    },
                    "metricset" : {
                      "period" : 60000,
                      "name" : "cpu"
                    },
                    "event" : {
                      "duration" : 294352,
                      "module" : "system",
                      "dataset" : "system.cpu"
                    }
                  }
                }
              ]
            }
          }
        },
        {
          "key_as_string" : "2022-02-14T06:40:00.000Z",
          "key" : 1644820800000,
          "doc_count" : 3,
```