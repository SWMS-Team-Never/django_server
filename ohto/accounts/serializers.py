from rest_framework import serializers
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample,extend_schema_serializer
from drf_spectacular.types import OpenApiTypes


#DONE: email UNIQUE 지정하기 -> models에서 필드에 unique=True로 지정하여 serializer에서 자동 검사하도록함.

User = get_user_model()

@extend_schema_serializer(
    examples=[
        OpenApiExample(
        "입력예시",
        description="create시 입력은 다음과 같다.",
        value={
            'username':'lux',
            'email':'test@gmail.com',
            'password':'1234',
            'phone_number':'01023452345'
        }
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
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) #db에서 조회하지 않도록 write_only 걸어준다.

    def create(self,validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])#user.password=validated_data['password']이런식으로 저장하면 인코딩없으므로 안됨
        user.email=validated_data['email']
        user.phone_number=validated_data['phone_number']
        user.save()
        return user
    class Meta:
        model=User
        fields=['pk','username','password','email','phone_number']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
        "조회(get)예시",
        description="get 출력은 유저 정보 담긴 Mypage 반환한다.",
        value={
            'username':'lux',
            'email':'test@gmail.com',
            'phone_number':'01023452345'
        }
    ),OpenApiExample(
        "수정(put)예시",
        description="수정(put) 입력은 다음과 같다 (출력은 입력대로 수정된 인스턴스 그대로 반환).",
        value={
            'username':'바꿀이름(str)',
            'email':'바꿀이메일(str)(ex:test@gmail.com)',
            'phone_number':'바꿀폰번호(01023452345)총 11자리여야한다'
        }
    )]
)
class MyPageSerializer(serializers.ModelSerializer):
    def update(self,instance,validated_data):
        instance.username=validated_data.get("username",instance.username)
        instance.phone_number=validated_data.get("phone_number",instance.phone_number)
        instance.save()
        return instance
    class Meta:
        model=User
        fields=['username','email','avatar_url','phone_number']
