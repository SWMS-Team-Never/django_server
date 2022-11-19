"""
WSGI config for instagram_clone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""
#NOTE: 1.settings.prod를 이용한다 -> 2. 커맨드는 guicorn --bind 0:8000 [프로젝트명].wsgi:application으로 구동
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ohto.settings.prod')

application = get_wsgi_application()
