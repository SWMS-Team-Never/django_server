from rest_framework import views,status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import redirect,get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from ..models import MoodTag, SituationTag, Song,PlayList,PlayListAndSongJoin, TopicTag
from ..serializers import PlayListSerializer
import json

class LandingPageView(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'music_demo/layout.html'

    def get(self,req):
        return Response({"index":True},status=status.HTTP_200_OK)

class FilterSongByTagView(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='music_demo/song_list.html'
    def get(self,req,tag_group,tag_name):
        tag_group_obj = [TopicTag,MoodTag,SituationTag]
        tag_name_list = ["topic_tag","mood_tag","situation_tag"]
        target = tag_name_list.index(tag_group)
        qs = tag_group_obj[target].objects.filter(tag_name=tag_name).values_list('song_id',flat=True)
        song_id_list = list(qs)
        songs = Song.objects.in_bulk(song_id_list)
        return Response({"songs":songs,"song_number":len(songs),"is_bulk":True})

class SongListView(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'music_demo/song_list.html'

    def get(self,req):
        search = req.GET.get('search',None)
        print(req.GET)
        qs = Song.objects.filter(Q(artist__icontains=search) | Q(title__icontains=search))
        return Response({"songs":qs,'song_number':len(qs),"is_bulk":False})

class MiniPlaylistsAPi(views.APIView):
    def get(self,req):
        qs = PlayList.objects.filter(owner=req.user)
        serializer = PlayListSerializer(qs,many=True)
        return Response(serializer.data)
    def post(self,req):
        title = req.POST.get('title',None)
        if title:
            PlayList.objects.create(title=title,owner=req.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#플레이리스트의 경우 따로 템플릿을 생성하지 않고 ajax통신으로 데이터 받을 수 있게끔한다.
class PlayListsApi(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='music_demo/playlist_list.html'
    def get(self,req):
        qs = PlayList.objects.filter(owner=req.user)
        return Response({"playlists":qs},status=status.HTTP_200_OK)
    def post(self,req):
        title = req.data.get("title",None)
        if title:
            PlayList.objects.create(title=title,owner=req.user)
            qs = PlayList.objects.filter(owner=req.user)
            return Response({"playlists":qs},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class PlayListAPI(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='music_demo/playlist.html'
    def get(self,req,pk):
        playlist = get_object_or_404(PlayList,pk=pk)
        song_id_list = []
        retrieve_song_id_qs = PlayListAndSongJoin.objects.filter(playlist_id=playlist.id)
        for song in retrieve_song_id_qs:
            song_id_list.append(song.song_id)
        songs = Song.objects.in_bulk(song_id_list)
        return Response({"songs":songs,"playlist":playlist})
    def post(self,req,pk):
        playlist = get_object_or_404(PlayList,pk=pk)
        playlist_id = playlist.id
        payload=req.data
        
        if payload["delete_option"]==1:
            songs_to_delete = payload["selected_songs"]
            print('delete mode')
            for song_id in songs_to_delete:
                qs = PlayListAndSongJoin.objects.filter(playlist_id=playlist_id,song_id=song_id).delete()
            return HttpResponseRedirect(reverse('playlist',kwargs={"pk":playlist_id}))
        songs_to_add = payload["selected_songs"]
        for song_id in songs_to_add:
            qs=PlayListAndSongJoin.objects.filter(playlist_id=playlist_id,song_id=song_id)
            if qs:
                continue
            PlayListAndSongJoin.objects.create(playlist_id=playlist_id,song_id=song_id)
        return HttpResponseRedirect(reverse('playlist',kwargs={"pk":playlist_id}))
    def delete(self,req,pk):
        playlist = get_object_or_404(PlayList,pk=pk)
        playlist_id= playlist.id
        songs_in_playlist = PlayListAndSongJoin.objects.filter(playlist_id=playlist_id)
        for song in songs_in_playlist:
            song.delete()
        playlist.delete()
        return HttpResponseRedirect(reverse('template/playlist_list'))
class UserPageView(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'music_demo/user_page.html'
    def get(self,req,user_name):
        page_user = get_object_or_404(get_user_model(),username=user_name,is_active=True)
        return Response({'page_user':page_user})

landing_page = LandingPageView.as_view()
song_list = SongListView.as_view()
mini_playlist=MiniPlaylistsAPi.as_view()
playlist_list = PlayListsApi.as_view()
