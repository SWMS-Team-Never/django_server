from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
import os

from music_demo.models import Song

class Command(BaseCommand):
    def handle(self,*args,**options):

        base_path = Path(__file__).resolve().parent.parent.parent
        csv_file_path = os.path.join(base_path,"data","for_django.csv")
        df = pd.read_csv(csv_file_path)
        for idx,row in df.iterrows():
            Song.objects.create(title=row["song"].strip(),artist=row["artist"].strip(),energy=int(row["e_label"]),valence=int(row["v_label"]))
        qs = Song.objects.all()
        print(f'song in file: {len(df)} created_song: {len(qs)}')



