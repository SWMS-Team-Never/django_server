from rest_framework import status
from rest_framework import permissions,views,viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

#TODO: 태그 검색구현하기
#TODO: api명세 
#NOTE: action 데코레이터로 viewset에서 커스텀 api구축 가능하다. ex)@action(detail=True,methods=["GET"])
from rest_framework.decorators import action

from django.db.models import Q 

import json

from ..serializers import PlayListSerializer, SongSerializer,PlayListSongJoinSerializer
from ..models import PlayList, Song, PlayListAndSongJoin

#NOTE: DRF에서는 as_view함수 호출시 django csrf_exepmt가 데코레이터로 감싸져 csrf체크를 하지 않는다.
#NOTE: api_view데코레어터로 작업하면 get,post.del,put 원하는 메소드만 명세하여 작업하므로 좀 가벼워진다.
#NOTE: APIView -> mixin -> generic -> viewset 으로 정리가 되어있고 mro(method resolution order)를 지키며 구성되어있다.
# Create your views here.

#커스텀 가능한 permission 객체
class IsOwner(permissions.BasePermission):
    def has_object_permssion(self,request,view,obj):
        return obj.owner == request.user

class SongSearchView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]
    @extend_schema(
        request=SongSerializer,
        responses={200:SongSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='search',description="query string 형식으로 보내며 키는 search로 보낸다."),
        ],
        summary='jwt 필요, search키 값에 들어온 제목이나 아티스트를 포함하는 곡들을 반환한다.',
        examples=[
            OpenApiExample(
            'search 쿼리스트링으로 검색할때.',
            description="쿼리스트링에 search 키값으로 제목이나 가수를 넘긴다.",
            value='/songs/search/?search=<str:검색값>'
        ),
        OpenApiExample(
            'search 검색 반환값.',
            description="곡중 제목이나 가수를 포함하는 곡들을 반환한다.",
            value=[
                {"id":1,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"},
                {"id":2,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"},
                {"id":3,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"}
                ]
        )]
    )
    def get(self,req,format=None):
        search=req.GET.get('search',None)
        qs = Song.objects.filter(Q(title__icontains=search) | Q(artist__icontains=search))
        serializer = SongSerializer(qs,many=True)
        return Response({"songs":serializer.data,"length":len(serializer.data)})

class PlayListView(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = [IsOwner,permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
    def perform_destroy(self, instance):
        #delete시 playlist안에 있는 노래까지 삭제
        instance_id = instance.id
        PlayListAndSongJoin.objects.filter(playlist_id=instance_id).delete()
        return super().perform_destroy(instance)
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡들을 반환한다.',
        examples=[
            OpenApiExample(
            "GET api 날리고 받는 json필드",
            description="song_list 키 안에 현재 플레이리스트에 들어있는 곡들의 id 리스트 받는다..",
            value={"song_list":[1,2,3,4,5,14,24]}
        )]
    )
    @action(detail=True,methods=['GET'])
    def get_songs(self,req,pk):
        #playlist/<int:playlist_id>/get_songs/로 접근하여 해당 playlist안에 곡들 반환
        instance = self.get_object()
        song_list = PlayListAndSongJoin.objects.filter(playlist_id=instance.id).values_list('song_id',flat=True)
        res = {"song_list":list(song_list)}
        print(type(song_list))
        return Response(data=res,status=status.HTTP_200_OK)
    @extend_schema(
        request=PlayListSerializer,
        responses={201:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='songs',description="플레이리스트 내에서 추가할 곡들의 id 리스트이다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡 중 추기하고 싶은 곡의 아이디를 넣자 -> 추가가 되었다.',
        examples=[
            OpenApiExample(
            "POST api 날릴때 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 추가할 곡 id 리스트 날리자.",
            value={"songs":[1,2,3,4,5,14,24]}
        ),OpenApiExample(
            "POST api 날리고 받는 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 추가할 곡 id 리스트 날리자.",
            value="아무것도 반환 하지 않는다 상태코드 201만 반환"
        )]
    )
    @action(detail=True,methods=["POST","PUT"])
    def insert_songs(self,req,pk):
        #playlist/<int:playlist_id>/insert_songs/로 접근하여 해당 playlist안에 곡 추가
        instance_id = self.get_object().id
        print(req.data)
        song_list = req.data.get("songs",None)
        #TODO: song_list비어있으면 redirect하기
        for id in song_list:
            join_serializer=PlayListSongJoinSerializer(data={"song_id":id,"playlist_id":instance_id})
            if join_serializer.is_valid():
                join_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='songs',description="플레이리스트 내에서 삭제할 곡들의 id 리스트이다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡 중 삭제하고 싶은 곡의 아이디를 넣자 -> 삭제가 되었다.',
        examples=[
            OpenApiExample(
            "delete api 날릴때 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 삭제할 곡 id 리스트 날리자.",
            value={"songs":[1,2,3,4,5,14,24]}
        )]
    )
    @action(detail=True,methods=["DELETE"])
    def delete_songs(self,req,pk):
        #playlist/<int:playlist_id>/delete_songs/로 접근하여 해당 playlist안에 선택한 곡 삭제
        instance_id = self.get_object().id
        song_list = req.data.get("songs",None)
        for song_id in song_list:
            qs = PlayListAndSongJoin.objects.get(song_id=song_id)
            qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #NOTE:기본 메서드 list,create,retrieve,update,partial_update,destroy 6가지 있음
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 토큰 담아서 get 요청하면 된다."),
        ],
        summary='jwt 필요, 유저가 현재 가지고 있는 플레이리스트 반환.',
        examples=[
            OpenApiExample(
            "list조회시",
            description="유저가 가지고 있는 플레이리스트 반환.",
            value=[
                {"id": 0,"title": "string","desc": "플레이리스트 설명string","cover_img": "img_url(str)"},
                {"id": 1,"title": "string","desc": "string","cover_img": "img_url(str)"},
                {"id": 2,"title": "string","desc": "string","cover_img": "img_url(str)"},]
        )]
    )
    def list(self,req,format=None):
        return super().list(req)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="입력한대로 플레이리스트 만들고 id필드 추가해서 같이 반환."),
        ],
        summary='jwt 필요, 입력한 대로 플레이리스트 생성.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 반환."),
        ],
        summary='jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 반환.',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 수정."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 수정. title은 필수필드 이므로 비워서는 안된다.',
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 수정."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 수정. title은 필수필드 이므로 비워서는 안된다.',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 삭제."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 삭제.',
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#아래 처럼 개별로 지정 할 수도있고 한꺼번에 router처리도 가능함
#playlist_list_view = PlayListListView.as_view({'get':'list'})





