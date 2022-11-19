<h2>환경 세팅</h2>

>manage.py 있는 경로에서  pip install -r requirements.txt입력 하여 패키지 다운로드

<h2>데이터 밀어넣기</h2>

>1. python3 manage.py dataframe_inject : 2000곡 sportify데이터 추가
>2. python3 manage.py json_data_inject : 1000곡 인수님 모델 출력 데이터 추가

<h2>swagger api 명세 url:</h2>

> '/api/schema/swagger-ui/' 로 접속한다

<h2>elasticsearch</h2>
1. install
> 1. pip install elasticsearch
> 2. elasticsearch-plugin install analysis-nori

2. data bulk하기
> 1. cd /django/search_music
> 2. python setting_bulk.py
>3. curl -H "Content-Type: application/json" -X POST -u elastic:changeme http://localhost:9200/_bulk\?pretty --data-binary @./data/input.json

3. search 방법
> music:
> - localhost:8000/music/?search=
> 
> plsylist:
> - localhost:8000/playlist/?search=
> 
 
<h2>실행 방법</h2>
> 1. docker-compose build
> 2. docker-compose up -d
> 3. cd django
> 4. python manage.py runserver
> 5. 다음 elasticsearch 위에 부분 순서대로 실행

서버 분리중이라 playlist 검색 기능은 누락된 상태