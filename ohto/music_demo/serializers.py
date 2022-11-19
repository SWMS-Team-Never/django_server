from rest_framework import serializers,validators
from .models import Song,PlayList,PlayListAndSongJoin
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample,extend_schema_serializer
from drf_spectacular.types import OpenApiTypes
#NOTE: ModelSerializer는 POST를 담당하는 Form으로 볼 수 있다.
class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['username','email','avatar_url']
        
class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ["id","title","desc","cover_img"]
        ordering = ['-created_at']

class PlayListSongJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayListAndSongJoin
        fields='__all__'
        validators=[
            validators.UniqueTogetherValidator(
                queryset=PlayListAndSongJoin.objects.all(),
                fields=["song_id","playlist_id"]
            )
        ]

@extend_schema_serializer(
    examples=[
        OpenApiExample(
        "list조회시",
        description="create시 입력은 다음과 같다.",
        value=[{'id':0,'title':'곡 제목(str)','artist':'가수(str)','tags':"['당당한','드라이브','운동']","youtube_link":"링크주소"},
        {'id':1,'title':'곡 제목(str)','artist':'가수(str)','tags':"['당당한','드라이브','운동']","youtube_link":"링크주소"},
        {'id':2,'title':'곡 제목(str)','artist':'가수(str)','tags':"['당당한','드라이브','운동']","youtube_link":"링크주소"}]
    ),OpenApiExample(
        "반환예시",
        description="create시 출력은 다음과 같다 (입력대로 생성된 인스턴스 그대로 반환).",
        value={
            'username':'lux',
            'email':'test@gmail.com',
            'password':'1234',
            'phone_number':'01023452345'
        }
    )]
)
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id','title','artist','youtube_link','tags']

#NOTE: serializer의 경우 모델을 조회하여 결과를 직렬화 해주는것이고 하나와 다수의 obj를 serializing 하는 방법이 다르다.
#NOTE: serializer.data의 경우 OrderedDict를 상속 받은 클래스이다.