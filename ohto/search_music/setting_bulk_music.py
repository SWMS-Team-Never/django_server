import requests, json, os
from elasticsearch import Elasticsearch

directory_path = 'path'
res = requests.get('http://localhost:9200')
es = Elasticsearch(
    hosts=['localhost:9200'],
    http_auth=('elastic', 'changeme'),
)

es.indices.create(
    index='music',
    body={
        # 한글 형태소 분석기 사용을 위해 토그나이저 설정
        "settings": {
            "index": {
                "analysis":{
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        # Elasticsearch 인덱스 타입 정의
        "mappings": {
            "properties":{
                "title": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "artist": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "tag": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "id": {
                    "type": "long"
                }
            }
        }
    }
)
import pandas as pd
# bulk를 위해 데이터 정제
directory_path = './data/'
def tran_data(name):
    df= pd.read_json(directory_path + name)
    tag=[]
    for topic, mood, situation in zip(df['topic'], df['mood'],df['situation']):
        tag.append(topic + ' ' + mood + ' ' + situation)
    df['tag'] = tag
    df = df.drop(['topic'], axis = 1)
    df = df.drop(['mood'], axis = 1)
    df = df.drop(['situation'], axis = 1)

    return df.to_json(force_ascii=False, orient = 'records', indent=4)


body = ""
count = 1
json_data = tran_data('music_tag.json')
parsed = json.loads(json_data)

for i in parsed:
    body = body + json.dumps({"index": {"_index": "music", "_id": count}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

f = open(directory_path + 'input.json', 'w')
f.write(body)
f.close()

es.bulk(body)