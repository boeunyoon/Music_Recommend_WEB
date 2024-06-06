import pymysql
import pandas as pd
import ast
import torch
from dataset.status_dataset import *
import numpy as np
from sqlalchemy import create_engine, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import multiprocessing
import sys, os
from collections import Counter
import random
import time
from concurrent.futures import ThreadPoolExecutor
import torch.nn.functional as F
sys.path.append('./recommander')
sys.path.append('./recommander/crawler')

# 데이터베이스 연결 문자열 생성
engine = create_engine("mysql+pymysql://root:950762@localhost/musicanalysis")
# 데이터베이스 연결 객체 생성
conn = engine.connect()



# 모델에 사용할 스탯 컬럼
status_cols = ['duration_ms', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
all_song_list = []

# 노래의 특징을 추출하는 모델
# 신경망 구조(입력크기, 은닉층, 출력크기)
# 선형 레이어와 ReLU 활성화 함수를 이용함
# self.acousticness_weight = torch.nn.Parameter(torch.tensor([2.0]))와 같이 스텟의 가중치의 조절이 가능함
# 빌보드 가중치 duration 0, acos 0.5, dance 0.3, energy 1.5, instru 0, liveness 0.5, loudness 1.8, speech 0.6, tempo 0, vanlance 0
class FeatureExtractor(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(FeatureExtractor, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, output_size)
        self.relu = torch.nn.ReLU()
        self.duration_ms_weight = torch.nn.Parameter(torch.tensor([0.1]))
        #self.acousticness_weight = torch.nn.Parameter(torch.tensor([1.8]))
        #self.danceability_weight = torch.nn.Parameter(torch.tensor([1.9]))
        self.energy_weight = torch.nn.Parameter(torch.tensor([1.9]))
        #self.instrumentalness_weight = torch.nn.Parameter(torch.tensor([1.1]))
        #self.liveness_weight = torch.nn.Parameter(torch.tensor([1.8]))
        #self.loudness_weight = torch.nn.Parameter(torch.tensor([1.1]))
        #self.speechiness_weight = torch.nn.Parameter(torch.tensor([1.1]))
        #self.tempo_weight = torch.nn.Parameter(torch.tensor([1.1]))
        #self.valence_weight = torch.nn.Parameter(torch.tensor([1.1]))

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out



# 2-1
# 데이터베이스에서 스텟 데이터를 DataFrame으로 가져오는 함수
def make_tensor_from_status(query, all='n'):
    # 쿼리 실행하여 노래 정보를 DataFrame으로 가져오기
    result = conn.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df_status = df[status_cols]
    #print(df_status)
    # 스탯 컬럼을 모델에 입력할 수 있는 형태로 변환
    status_tensor = torch.tensor(df_status.values[1:], dtype=torch.float32)
    status_dataset = StatusDataset(status_tensor)
    status_dataloader = DataLoader(status_dataset, batch_size=32, shuffle=False)

    if all=='y':
        return status_dataloader, df
    

    return status_dataloader

# 2-2
# 학습 데이터의 특징 추출
# FeatureExtractor 클래스를 이용하여 입력 데이터를 모델에 전달하고, 모델의 출력으로부터 특징 벡터를 추출
def extract_feature_from_input(status_dataloader):
    model = FeatureExtractor(input_size=10, hidden_size=32, output_size=32)

    features = []
    for batch in status_dataloader:
        # 모델에 입력 데이터 전달하여 특징 벡터 계산
        output = model(batch)
        # 계산된 특징 벡터를 리스트에 추가
        features.append(output)

    # 리스트를 하나의 텐서로 결합
    features = torch.cat(features, dim=0)
    
    #print("* 학습 데이터의 특징--------------------")
    #print(features)

    return features

# 2-3
# 추천 대상 데이터의 특징 추출
# FeatureExtractor 클래스를 이용하여 입력 데이터를 모델에 전달하고, 모델의 출력으로부터 특징 벡터를 추출
def extract_feature_from_output(status_dataloader):
    # 특징 추출기 모델을 생성
    model = FeatureExtractor(input_size=10, hidden_size=32, output_size=32)

    # 추천 대상 노래들의 특징 벡터를 계산
    song_features = []
    for status in status_dataloader:
        # 스탯 정보를 텐서로 변환
        inputs = torch.tensor(status).float()

        # 모델에 입력 데이터 전달하여 특징 벡터 계산
        output = model(inputs)

        # 계산된 특징 벡터를 리스트에 추가
        song_features.append(output)
    
    song_features = torch.cat(song_features, dim=0)
    print("* 전체 데이터의 특징--------------------")

    return song_features

# 2
# track_id 리스트를 입력으로 받아, 해당 트랙들을 기반으로 추천할 노래들의 ID를 찾아내는 함수. 
# 이 함수는 학습 데이터와 추천 대상 데이터 간의 유사도를 측정하고, 유사도가 높은 상위 num개의 track_id를 반환
def primary_recommand(track_id_list, num=7, except_track_list = []):
    seed = int(time.time())
    print("시드: ",seed)
    random.seed(seed)
    torch.manual_seed(seed)
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    model_query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    AND energy IS NOT NULL
    """)


    # 2-2 입력 데이터의 특징 추출
    model_status_data_loader = make_tensor_from_status(model_query)
    model_feature = extract_feature_from_input(model_status_data_loader)#.unsqueeze(0).detach().numpy()

    if except_track_list != []:
        track_id_list.extend(except_track_list)
    track_ids_str = ','.join(f"'{song_id}'" for song_id in track_id_list)
    #all_song_query = text(f"""
    #SELECT * FROM song_status 
    #WHERE id NOT IN ({track_ids_str})
    #""")

    all_song_query = text(f"""
    SELECT * FROM song_status WHERE id IN (SELECT id FROM songs WHERE popularity > 50) and id NOT IN ({track_ids_str})
    """)



    # 2-3 추천 대상 데이터의 특징 추출
    all_song_status_data_loader, df = make_tensor_from_status(all_song_query, all='y')
    all_song_feature = extract_feature_from_output(all_song_status_data_loader)#.unsqueeze(0).detach().numpy()

    # 리스트를 하나의 텐서로 결합
    similarity_matrix = torch.matmul(all_song_feature, model_feature.t())
    _, indices = torch.topk(similarity_matrix, num, largest=True, dim=1)
    song_indices = indices[0].tolist()
    song_ids = df.iloc[song_indices]['id'].tolist()
    
    
    return song_ids

# 3 
# song_ids 리스트를 입력으로 받아, 해당 노래들의 장르 정보를 데이터베이스에서 가져옴. 
# song_ids와 해당 노래의 장르를 튜플 형태로 반환
def get_song_genres(song_ids):
    #placeholders = ', '.join(['%s'] * len(song_ids))
    query = text(f"SELECT song_id, genre FROM song_genres WHERE song_id IN :ids")
    params = {"ids": tuple(song_ids)}
    result = conn.execute(query, params)
    results = result.fetchall()
    
    return results

# 4-1
# track_id 리스트를 입력으로 받아, 해당 노래들의 장르 정보를 데이터베이스에서 가져와 장르별로 개수를 세는 함수
# 노래들이 속한 장르들의 빈도를 계산
def get_songs_genres_count(track_id_list):
    
    genre_list = []
    for track_id in track_id_list:
        query = text("SELECT genre FROM song_genres WHERE song_id = :track_id")
        result = conn.execute(query.bindparams(track_id=track_id))
        results = result.fetchall()
        
        for row in results:
            genre_list.append(row[0])
    
    genre_count = Counter(genre_list)
    #print(genre_count)
    return genre_count

# 4 추천 학습 목록이 사용자의 재생목록일 경우
# 사용자의 재생목록으로부터 상위 3개의 장르를 추출하는 함수
def get_top3_genres_from_track_list(track_id_list):
    genre_count = get_songs_genres_count(track_id_list)
    top_genres = [genre for genre, count in genre_count.most_common(3)]
    print("* 탑 장르 3----------------------------")
    print(top_genres)

    return top_genres




# 5
# 추천 대상 노래들과 상위 장르들을 비교하여, 상위 장르에 속하는 노래들만 필터링하여 반환하는 함수
def filter_songs_by_genre(songs, top_genres):
    filtered_songs = []
    if "pop" in top_genres:
        # "pop"을 리스트에서 제거
        top_genres.remove("pop")
        print(top_genres)
    for song in songs:
        song_id, song_genre = song
        
        if song_genre in top_genres:
            if song_id not in filtered_songs:
                filtered_songs.append(song_id)

    return filtered_songs


# 6
# track_id 리스트를 입력으로 받아, 해당 노래들을 인기도(popularity)에 따라 내림차순으로 정렬하여 반환하는 함수
def sort_by_popularity(filtered_songs):
    placeholders = ', '.join([':id{}'.format(i) for i, _ in enumerate(filtered_songs)])
    query = text(f"SELECT id, popularity, title, artist, album, release_date, 300px FROM songs WHERE id IN ({placeholders})")
    params = {f"id{i}": song_id for i, song_id in enumerate(filtered_songs)}
    result = conn.execute(query, params)
    results = result.fetchall()
    sorted_songs = results
    #sorted_songs = sorted(results, key=lambda x: x[1], reverse=True)
    print("* 인기도 순으로 정렬--------------------")

    return sorted_songs

# 1
# primary_recommand 함수를 호출하여 추천 대상 노래들의 ID를 얻고, 해당 노래들의 장르 정보를 가져와 상위 장르들을 추출 
# filter_songs_by_genre 함수를 이용하여 상위 장르에 속하는 노래들만 필터링 
# sort_by_popularity 함수를 호출하여 추천 노래들을 인기도에 따라 정렬하여 최종 추천 결과를 반환
# 현재는 장르로 노래를 추출하는 것을 제외함
def recommand_from_tracklist(track_id_list, num):
    song_ids = primary_recommand_new(track_id_list, num)
    
    #else:
    #    seed = int(time.time())
    #    random.seed(seed)
    #    # 앞 10개 요소를 무작위로 섞기
    #    random.shuffle(song_ids)

        # 섞인 리스트 중에서 앞의 절반 가져오기
    #    half_length = len(song_ids) // 2
    #    random_half = song_ids[:half_length]
    #    print("앞절반", random_half)
    #    num = num + len(random_half)
    #    track_id_list.extend(random_half)
    #    remaining_half = song_ids[half_length:]
    #    print("나머지 절반", remaining_half)
    #    song_ids = primary_recommand(track_id_list, num, remaining_half)
    #    song_ids.extend(remaining_half)

    
    genres = get_song_genres(song_ids)
    
    #top_genres = get_top3_genres_from_billboard(start_date, end_date)
    top_genres = get_top3_genres_from_track_list(track_id_list)
    top_genres = get_top3_genres_from_track_list(song_ids)

    #print("* 장르로 추출--------------------------")
    #print("실행 전", len(song_ids))
    #print("실행 후", len(filtered_songs))

    sorted_songs = sort_by_popularity(song_ids)
    sorted_ids = [song[0] for song in sorted_songs]

    recommand_songs_json = []
    for song in sorted_songs:
        json_data = {
            "title": song[2],
            "artist": song[3],
            "album": song[4],
            "release_date": song[5],
            "image": song[6]
        }
        recommand_songs_json.append(json_data)
    for song in recommand_songs_json:
        print(song['title'], ':',song['artist'])
    
    
    return recommand_songs_json

# 데이터 베이스의 플레이리스트와 입력된 플레이리스트를 비교해 추천한다.
def primary_recommand_new(track_id_list, num = 20):
    seed = int(time.time())
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)

    # 입력 데이터의 특징 추출
    input_data_loader = make_tensor_from_status(query)
    input_feature = extract_feature_from_input(input_data_loader)
    
    all_song_query = text(f"""
    SELECT id, duration_ms, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence FROM song_status WHERE id IN (SELECT id FROM songs WHERE popularity > 50) and id NOT IN ({track_ids_str})
    ORDER BY RAND({seed}) LIMIT 8000""")
    all_song = conn.execute(all_song_query)
    all_song = all_song.fetchall()

    
    model = FeatureExtractor(input_size=10, hidden_size=32, output_size=32)
    result = []
    # 데이터베이스의 플레이리스트들을 각각 입력된 플레이리스트와 코사인 유사도 비교를 시행한다.
    for data in all_song:
        # 데이터베이스 플레이리스트 특징 추출
        track_id = data[0]
        data_tensor = torch.tensor(data[1:], dtype=torch.float32)
        data_feature = model(data_tensor)
        data_feature = data_feature.view(1, -1)
        cosine_similarities = compute_cosine_similarity(data_feature, input_feature)
        # 코사인 유사도 비교
    
        #similarity = compute_cosine_similarity(input_feature, data_feature)
        result.append((track_id, np.array(cosine_similarities)))
    


    # 유사도 비교의 결과값에 따라 플레이리스트 정렬
    sorted_data = sorted(result, key=lambda x: max(x[1][:, 1]), reverse=True)
    track_ids = [item[0] for item in sorted_data[:num]]


    return track_ids

# 코사인 유사도를 이용해 플레이리스트 간의 유사도를 텐서로 측정한다.
def compute_cosine_similarity(tensor1, tensor2):
    similarity = cosine_similarity(tensor1.detach().numpy(), tensor2.detach().numpy())
    return similarity

# 데이터 베이스의 플레이리스트와 입력된 플레이리스트를 비교해 추천한다.
def compare_playlists(track_id_list, num = 6):
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)

    # 입력 데이터의 특징 추출
    input_data_loader = make_tensor_from_status(query)
    input_feature = extract_feature_from_input(input_data_loader)
    
    playlist_query = text(f"""
    SELECT * FROM spotify_playlist
    """)
    playlist = conn.execute(playlist_query)
    playlist = playlist.fetchall()

    result = []
    # 데이터베이스의 플레이리스트들을 각각 입력된 플레이리스트와 코사인 유사도 비교를 시행한다.
    for data in playlist:
        track_list = ast.literal_eval(data[2])

        track_ids_str = ','.join([f"'{track_id}'" for track_id in track_list])

        # 데이터베이스 플레이리스트 특징 추출
        playlist_data_loader = make_tensor_from_status(query)
        playlist_feature = extract_feature_from_input(playlist_data_loader)

        # 코사인 유사도 비교
        similarity = compute_cosine_similarity(input_feature, playlist_feature)
        result.append((data[0], np.array(similarity), data[1], data[2], data[3]))

    
    # 유사도 비교의 결과값에 따라 플레이리스트 정렬
    sorted_data = sorted(result, key=lambda x: max(x[1][:, 1]), reverse=True)


    json_data_list = []
    for i in range(0,num):
        json_data = {
            "id": sorted_data[i][0],
            "name": sorted_data[i][2],
            "track_list": sorted_data[i][3],
            "image": sorted_data[i][4]
        }

        json_data_list.append(json_data)
    
    return json_data_list

def compare_playlists_final(track_id_list, num = 6):
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)

    # 입력 데이터의 특징 추출
    input_data_loader = make_tensor_from_status(query)
    input_feature = extract_feature_from_input(input_data_loader).detach().numpy()
    
    playlist_query = text(f"""
    SELECT * FROM spotify_playlist
    """)
    playlist = conn.execute(playlist_query)
    playlist = playlist.fetchall()

    playlist_features = []
    artist_information = []
    # 데이터베이스의 플레이리스트들을 각각 입력된 플레이리스트와 코사인 유사도 비교를 시행한다.
    for data in playlist:
        track_list = ast.literal_eval(data[2])

        track_ids_str = ','.join([f"'{track_id}'" for track_id in track_list])

        # 데이터베이스 플레이리스트 특징 추출
        playlist_data_loader = make_tensor_from_status(query)
        playlist_feature = extract_feature_from_input(playlist_data_loader).detach().numpy()
        playlist_features.append(playlist_feature)
        artist_information.append((data[0], data[1], data[2], data[3]))

    similarity_matrix = cosine_similarity(input_feature, playlist_features)

    similarity_results = []
    for track_name, similarity_value in zip(artist_information, similarity_matrix):
        similarity_results.append((track_name, similarity_value))
    # 유사도 비교의 결과값에 따라 플레이리스트 정렬
    sorted_data = sorted(similarity_results, key=lambda x: max(x[1][:, 1]), reverse=True)


    json_data_list = []
    for i in range(0,num):
        json_data = {
            "id": sorted_data[i][0],
            "name": sorted_data[i][2],
            "track_list": sorted_data[i][3],
            "image": sorted_data[i][4]
        }

        json_data_list.append(json_data)
    
    return json_data_list

def process_playlist(data, input_feature):
    track_list = ast.literal_eval(data[2])
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)
    
    # 데이터베이스 플레이리스트 특징 추출
    playlist_data_loader = make_tensor_from_status(query)
    playlist_feature = extract_feature_from_input(playlist_data_loader)
    
    # input_feature를 CPU로 이동
    input_feature_cpu = input_feature.to('cpu')

    similarity = compute_cosine_similarity(input_feature, playlist_feature)
    
    
    return (data[0], np.array(similarity), data[1], data[2], data[3])

def compare_playlist_by_multiprocess(track_id_list, num = 6):
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)

    # 입력 데이터의 특징 추출
    input_data_loader = make_tensor_from_status(query)
    input_feature = extract_feature_from_input(input_data_loader)
    input_feature = input_feature.detach()  # 그래디언트 추적 중지
    input_feature = input_feature.to('cpu')  # CPU로 이동
    
    playlist_query = text(f"""
    SELECT * FROM spotify_playlist
    """)
    playlist = conn.execute(playlist_query)
    playlist = playlist.fetchall()
    
    # CPU 코어 수만큼 프로세스를 생성하여 병렬 처리
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = []
        
        for data in playlist:
            result = pool.apply_async(process_playlist, args=(data, input_feature))
            
            results.append(result)
            

        # 모든 프로세스가 완료될 때까지 대기
        pool.close()
        pool.join()
        sorted_data = []

        for result in results:
            try:
                data = result.get()
                sorted_data.append(data)
            except Exception as e:
                # 예외 처리: NaN 값을 처리하거나 해당 결과를 무시하거나 다른 작업을 수행
                pass
    # 유사도 비교의 결과값에 따라 플레이리스트 정렬
    sorted_data = sorted(sorted_data, key=lambda x: max(x[1][:, 1]), reverse=True)

    json_data_list = []
    for i in range(0,num):
        json_data = {
            "id": sorted_data[i][0],
            "name": sorted_data[i][2],
            "track_list": sorted_data[i][3],
            "image": sorted_data[i][4]
        }

        json_data_list.append(json_data)
    
    return json_data_list

# 데이터 베이스의 플레이리스트와 입력된 플레이리스트를 비교해 추천한다.
def compare_artists(track_id_list, num = 5):
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)

    # 입력 데이터의 특징 추출
    input_data_loader = make_tensor_from_status(query)
    input_feature = extract_feature_from_input(input_data_loader)
    
    artist_songs_query = text(f"""
    SELECT id, songs FROM artist_songs WHERE CHAR_LENGTH(songs) >= 100 and popularity > 75
                              ORDER BY popularity DESC
    """)
    artist_songs = conn.execute(artist_songs_query)
    artist_songs = artist_songs.fetchall()

    result = []
    # 데이터베이스의 플레이리스트들을 각각 입력된 플레이리스트와 코사인 유사도 비교를 시행한다.
    for data in artist_songs:
        track_list = ast.literal_eval(data[1])

        track_ids_str = ','.join([f"'{track_id}'" for track_id in track_list])

        # 데이터베이스 플레이리스트 특징 추출
        artist_songs_data_loader = make_tensor_from_status(query)
        artist_songs_feature = extract_feature_from_input(artist_songs_data_loader)

        # 코사인 유사도 비교
        similarity = compute_cosine_similarity(input_feature, artist_songs_feature)
        print(similarity)
        result.append((data[0], np.array(similarity)))


    # 유사도 비교의 결과값에 따라 플레이리스트 정렬
    sorted_data = sorted(result, key=lambda x: max(x[1][:, 1]), reverse=True)
    sorted_data = sorted_data[:num]

    result = []
    artist_list = []
    for data in sorted_data:
        artist_id = data[0]
        artist_query = text(f"""
        SELECT * FROM artist WHERE id = '{artist_id}'
        """)

        artist = conn.execute(artist_query)
        artist = artist.fetchall()

        artist_json = {
            "id": artist[0][0],
            "name": artist[0][1],
            "image": artist[0][3]
        }
        artist_list.append(artist[0][1])
        result.append(artist_json)

    return artist_list

# 트랙리스트에서 아티스트의 수 세기
def get_songs_artist_count(track_id_list):
    
    artist_list = []
    # 트랙 아이디에서 아티스트 이름 가져오기
    for track_id in track_id_list:
        query = text("SELECT artist FROM songs WHERE id = :track_id")
        result = conn.execute(query.bindparams(track_id=track_id))
        results = result.fetchall()
        
        for row in results:
            artist_list.append(row[0])
    
    # 가져온 아티스트 이름을 세기
    artist_count = Counter(artist_list)

    # 가장 많은 아티스트 5명의 데이터를 json화
    top_artist = [artist for artist, count in artist_count.most_common(5)]

    result =[]
    for artist in top_artist:
        query = text("SELECT * FROM artist WHERE name = :name")
        info = conn.execute(query.bindparams(name=artist))
        info = info.fetchall()
        if info == []:
            continue
        info_json = {
            "id": info[0][0],
            "name": info[0][1],
            "image": info[0][3]
        }
        result.append(info_json)

    #print(genre_count)
    return result

def get_2023_billobard_track_list():
    dates = ["2023-01-15", "2023-02-15", "2023-03-15", "2023-04-15", "2023-06-15", "2023-07-15", "2023-08-15", "2023-09-15", "2023-10-15"]

    result = []
    for date in dates:
        query = text(f"""
        SELECT billboard_data FROM billboard WHERE billboard_date = '{date}'
        """)
        track_list = conn.execute(query)
        track_list = track_list.fetchall()
        track_list = ast.literal_eval(track_list[0][0])
        track_id_list = [d['track_id'] for d in track_list]
        result.extend(track_id_list)
    result = list(set(result))
    
    return result

def calculate_stat_trends(track_id_list, filename = "input.png"):
    track_ids_str = ','.join([f"'{track_id}'" for track_id in track_id_list])
    model_query = text(f"""SELECT s.artist, s.title, ss.duration_ms, ss.acousticness, ss.danceability, ss.energy, ss.instrumentalness, ss.liveness, ss.loudness, ss.speechiness, ss.tempo, ss.valence
    FROM songs s
    JOIN song_status ss ON s.id = ss.id
    WHERE s.id IN ({track_ids_str})
    """)
    result = conn.execute(model_query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df_status = df[status_cols]
    #print(df_status)
    # 스탯 컬럼을 모델에 입력할 수 있는 형태로 변환
    status_tensor = torch.tensor(df_status.values[1:], dtype=torch.float32)

    # 평균과 표준 편차 계산
    mean = torch.mean(status_tensor, dim=0)
    std = torch.std(status_tensor, dim=0)

    # 데이터 표준화
    standardized_data = (status_tensor - mean) / std
    #print(standardized_data)
    # 각 스텟의 경향성 시각화
    # 모든 그래프를 하나의 이미지로 병합하고 저장
    # 모든 그래프를 하나의 이미지로 병합하고 저장
    fig, axes = plt.subplots(2, len(status_cols) // 2, figsize=(12, 8))

    for i, stat_col in enumerate(status_cols):
        row, col = divmod(i, len(status_cols) // 2)  # 2개의 행으로 나누어 배치
        axes[row, col].hist(standardized_data[:, i], bins=20)
        axes[row, col].set_title(f"{stat_col}")
        axes[row, col].set_xlabel("Standardized Value")
        axes[row, col].set_ylabel("Frequency")

    plt.tight_layout()  # 그래프가 겹치지 않도록 조정

    plt.savefig("status_trends/status_trends "+ filename)
    plt.show()

track_list = ["1A8bKLSq6A4OboABhnDN6Q", "1PHfBYe9DTQzaI53JJS9GP", "5IbMUI4rcWtXlq83UWqTcQ", "6DoGtGyDgv5mVxeCpP92tX", "42NjsYhyIo0UVl3dkAQ0Im","0QG8SAdaB9NcoM811HDq1S","6Pgmqg15yVexuOgtzuxwoX","1OEEIcF2Q2aK0zZNnFmc05","07js7XK2UIgj3YQzOuGnZS", "0wbDgMuAoy7O7pL3a69uZx"]

#calculate_stat_trends(track_list)
#compare_playlists(track_list)
#id = recommand_from_billboard("2023-03-01", "2023-03-02") #빌보드 차트로
#track_list = ["2pIUpMhHL6L9Z5lnKxJJr9", "65FftemJ1DbbZ45DUfHJXE", "0fv2KH6hac06J86hBUTcSf", "0u2P5u6lvoDfwTYjAADbn4", "4P9Q0GojKVXpRTJCaL3kyy", "7qEHsqek33rTcFNT9PFqLf", "4sx6NRwL6Ol3V6m9exwGlQ", "0wI7QkCcs8FUQE1OkXUIqd", "2ekn2ttSfGqwhhate0LSR0", "6I3mqTwhRpn34SLVafSH7G", "0fX4oNGBWO3dSGUZcVdVV2"]
#id = recommand_from_tracklist(get_2023_billobard_track_list(),30) #재생 목록으로
