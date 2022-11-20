import pandas as pd
import json
# bulk를 위해 데이터 정제
directory_path = 'data/'
def tran_data(name):
    df = pd.read_json(directory_path + name)
    tag=[]
    for topic, mood, situation in zip(df['topic'], df['mood'],df['situation']):
        tag.append(topic + ' ' + mood + ' ' + situation)
    df['tag'] = tag
    df = df.drop(['topic'], axis = 1)
    df = df.drop(['mood'], axis = 1)
    df = df.drop(['situation'], axis = 1)

    # add tag

    return df.to_json(force_ascii=False, orient = 'records', indent=4)

tag=[]
df = pd.read_json(directory_path+'meta_list.json')
df2 = pd.read_json(directory_path+'music_tag.json')
for topic, mood, situation, genre, date in zip(df2['topic'], df2['mood'], df2['situation'], df['album_genre'], df['release_date']):
    m = date[5:6]
    if date[6] != '.':
        m=date[5:7]

    if 2 < int(m) < 6:
        date = '봄'
    elif 5 < int(m) < 9:
        date = '여름'
    elif 8 < int(m) < 12:
        date = '가을'
    else:
        date = '겨울'
    tag.append(topic + ' ' + mood + ' ' + situation + ' ' + genre + ' ' + date)

df['tag'] = tag
df = df.drop(['album_genre'], axis = 1)
df = df.drop(['release_date'], axis = 1)
df = df.drop(['album_title'], axis = 1)
df = df.drop(['track_id'], axis = 1)
df = df.drop(['play_time'], axis = 1)

df = df.rename(columns={'artists':'artist'})
df = df.rename(columns={'track_title':'title'})


json_data = df.to_json(force_ascii=False, orient = 'records', indent=4)
parsed = json.loads(json_data)

body = ""
count = 1

for i in parsed:
    body = body + json.dumps(i, ensure_ascii=False) + '\n'

f = open(directory_path + 'music_data.json', 'w')
f.write(body)
f.close()

"""
json_data = tran_data('music_tag.json')
parsed = json.loads(json_data)

for i in parsed:
    body = body + json.dumps({"index": {"_index": "music", "_id": count}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

f = open(directory_path + 'input.json', 'w')
f.write(body)
f.close()

"""