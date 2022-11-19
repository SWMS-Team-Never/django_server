from django.core.management import BaseCommand
from pathlib import Path
import os
import json

from music_demo.models import TopicTag,MoodTag,SituationTag

class Command(BaseCommand):
    def handle(self,*args,**options):
        qsT = TopicTag.objects.order_by('tag_name').values('tag_name').distinct()
        qsM = MoodTag.objects.order_by('tag_name').values('tag_name').distinct()
        qsS = SituationTag.objects.order_by('tag_name').values('tag_name').distinct()


        test_dict = {}
        keys=["topic_tag","mood_tag","situation_tag"]
        vals=[]
        for el in (qsT,qsM,qsS):
            vals.append(list(el.values_list("tag_name",flat=True)))
        for i in range(3):
            test_dict.update({f"{keys[i]}":vals[i]})
        print(test_dict)
        data = json.dumps(test_dict)
        base_path = Path(__file__).resolve().parent.parent.parent
        save_file_dir = os.path.join(base_path,'static','song_tag')
        with open(save_file_dir+'/song_tag.json','w') as f:
            f.write(data)