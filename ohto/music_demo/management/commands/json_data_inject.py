from lib2to3.pytree import Base
from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
import os

from music_demo.models import Song,TopicTag,SituationTag,MoodTag

class Command(BaseCommand):
    help="insert csv files data into database"

    def handle(self,*args,**options):
        base_path= Path(__file__).resolve().parent.parent.parent
        dataframe_path = os.path.join(base_path,'data','test.json')
        df = pd.read_json(dataframe_path)
        for idx,row in df.iterrows():
            if idx <2:
                continue
            title = row["title"]
            artist = ""
            if len(row["artist"])>1:
                for el in row["artist"]:
                    artist+=f" {el}"
                artist = artist.lstrip()
            else:
                artist = row["artist"][0]
            new_song = Song(title=title,artist=artist)
            new_song_id = new_song.id
            #NOTE: tags필드에 하나의 리스트로 다 때려 넣었다.
            #obj_list = [TopicTag,MoodTag,SituationTag]
            obj_name_list = ["topic","mood","situation"]
            tag_list = []
            for i in range(3):
                #obj_list[i].objects.create(song_id=new_song_id,tag_name=row[f"{obj_name_list[i]}"])
                tag_list.append(row[f"{obj_name_list[i]}"])
            new_song.tag_list=tag_list
            new_song.save()
        qs = Song.objects.filter(energy=-1)        
        print(f"song in data: {len(df)} created song:{len(qs)} ")
