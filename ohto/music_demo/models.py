from django.conf import settings
from django.db import models

import json

# Create your models here.
class Song(models.Model):
    #TODO: 음악 앨범 커버 필드 더하기
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=150)
    youtube_link = models.URLField(blank=True)
    energy = models.IntegerField(default=-1)
    valence = models.IntegerField(default=-1)
    album_cover = models.ImageField(blank=True, upload_to='album_covers/%Y/%m')
    tags = models.CharField(max_length=250,blank=True)
    @property
    def tag_list(self):
        return json.loads(self.tags)
    @tag_list.setter
    def tag_list(self,tag_list):
        self.tags=json.dumps(tag_list,ensure_ascii=False)
#TODO:  split 
"""
class Song_tag:
    tag = models
    energy = models.
    valence = 
"""

class PlayList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='playlist_owner')
    title = models.CharField(max_length=150)#FIXME set default title regulary
    created_at = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(blank=True)
    cover_img = models.ImageField(blank=True,upload_to="playlists/cover_images/%Y/%m")

class PlayListAndSongJoin(models.Model):
    playlist_id = models.IntegerField(default=0)
    song_id = models.IntegerField(default=0)

class PlayListTag(models.Model):
    playlist_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=100)
    #삭제 같은 경우에 playlist삭제시 이 테이블 다 조회해서 삭제한다
    #또는 플레이리스트 자체 수정일 때는 id 넘겨서 삭제해도 된다.

class TopicTag(models.Model):
    song_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=100)
class MoodTag(models.Model):
    song_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=100)
class SituationTag(models.Model):
    song_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=100)