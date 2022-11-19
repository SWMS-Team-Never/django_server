from .common import *
#안티 패턴이지만 settings 에서는 모든 파일을 임포트 해와야 하므로 허용한다.

#TODO:Let's encrypt로 ssl인증 발급

#docker run 시
#NOTE: 데이터 옮길때 mysql 설정: docker run -d -p 3306:3306 --name django-mysql -v `pwd`/data:/var/lib/mysql mysql

#NOTE: linux os 환경변수 설정: /etc -> cat << EOD >> bash.bashrc -> export PROD=--settings=...

#NOTE: 1. docker run -it --name django-main -p 8000:8000 --link django-mysql django-main
#NOTE: 2. docker start -i django-main

#vim 설치방법
#NOTE: 1.apt-get update -> 2.apt-get install vim

#db 구성시
#NOTE: CREATE DATABASE <dbname> CHARACTER SET utf8;

#prod setting migration할 때 
#NOTE: python3 manage.py makemigrations $PROD -> python3 manage.py migrate $PROD

#TODO:이미지 환경변수 env ['PROD','P3M']에 추가하기 

#TODO:docker image hub에  django project 이미지 배포하기

#NOTE: prod 환경 설정시 debug false하여 메모리에 쿼리 누적되는것 방지 -> allowed-hosts에 지정된 호스트들만 접근 가능하게 설정
DEBUG = os.environ.get('DEBUG') in ['true','True']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ohto_db',
        'USER': 'ohto',
        'PASSWORD': 'Never123',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

#TODO: 1.error 로그 관리 sentry서비스 이용하여 체계적으로 관리 될 수 있도록 하자.
LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "handlers":{"console":{"level":"ERROR", "class":"logging.StreamHandler"}},
    "loggers":{"django":{"handlers":["console"],"level":"ERROR"}}
}