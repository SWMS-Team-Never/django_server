from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SignUpSerializer,MyPageSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
#TODO: jwt인증 방식을 username -> email로 바꾸기
#TODO: avatar 저장할 static file nginx에서 작업하기

User = get_user_model()
class SignUpView(CreateAPIView):
    model=get_user_model()
    serializer_class=SignUpSerializer
    permission_classes=[AllowAny]

    @extend_schema(
        request=SignUpSerializer,
        responses={201:SignUpSerializer},
        parameters=[
            OpenApiParameter(name='username',description="닉네임 필드로사용하고 단순히 str입력이다."),
            OpenApiParameter(name='phone_number',description="010-?\d{4}-?\d{4} 꼴로 전화번호 받는다 '-' 없이 다 붙여서 넣는다.")
        ],
        description='유저 생성전용 api이므로 입력만 유의하면 된다. 반환값은 생성된 유저 인스턴스이다.',
        summary='회원가입 api, 유일하게 jwt필요없다.'
    )
    def post(self,req):
        return super().post(req)

class MyPageView(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(
        request=OpenApiParameter.HEADER,
        responses={200:MyPageSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 토큰 담아서 get 요청하면 된다."),
        ],
        summary='jwt 필요, 유저 mypage에 담길 정보 반환.'
    )
    def get(self,req,format=None):
        user_id=req.user.id
        instance = User.objects.get(pk=user_id)
        serializer=MyPageSerializer(instance=instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @extend_schema(
        request=MyPageSerializer,
        responses={202:MyPageSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 토큰 담아서 get 요청하면 된다."),
            OpenApiParameter(name='username',description="수정할 닉네임 단순히 str입력이다."),
            OpenApiParameter(name='phone_number',description="수정할 폰번호이고 010-?\d{4}-?\d{4} 꼴로 전화번호 받는다 '-' 없이 다 붙여서 넣는다.")
        ],
        summary='jwt 필요, 수정한 유저정보 그대로 mypage수정.'
    )
    def put(self,req,format=None):
        user_id=req.user.id
        instance=User.objects.get(pk=user_id)
        serializer=MyPageSerializer(instance,data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

