import sys, os
sys.path.append('./recommander')
sys.path.append('./recommander/crawler')
from dbconnect import *
from recommand import *
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import base64
from urllib.parse import urlencode
import ast
import json
import pymysql
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import itertools
import numpy as np
import time


#Spotify 권한
cid = '01b9ce28405042deb84a4813e63d557d'
secret = 'd20308c58757497191c1386264672528'

#cid = '133e17352a85443a803690b5adaff2c4'
#secret = 'e1bf131abfce43999e5ff0df91ac388a'

#cid = '602eea5cabdd444ca3d18e573db1a9f9'
#secret = '9d34d00765a54dc78dc129abeba884a8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

# spotipy 라이브러리로 spotify의 노래 스텟을 가져오는 클래스
class Spotify_audio_features:
    # 권한 획득
    def __init__(self):
        # initial setting
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # db 연결
    def connect_cursor(self):
        # MySQL 데이터베이스 연결
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='950762',
            db='musicanalysis'
        )
        self.cur = self.conn.cursor()

    # db 연결 끊기
    def close_cursor(self):
        self.cur.close()
        self.conn.close()

    # 노래 제목으로 노래 정보를 가져오는 함수
    def get_song_data(self, title, limit=1):

        # 제목으로 트랙 정보 가져오기
        track_info = self.sp.search(q=title, limit=limit, type='track', market='US')
        if track_info["tracks"]["items"] == []:
            #특수문자 검사
            title = str(title)
            title = title.replace('*', 'i')
            track_info = self.sp.search(q=title, type='track', market='US')
            
            #재검사 이후에도 검색 결과가 없으면 None 반환
            if track_info["tracks"]["items"] == []:
                return None, None, None


        json_length = len(track_info["tracks"]["items"])
        song_list_data = []
        genre_list_data = []
        album_image_list_data = []

        for i in range(0, json_length):

            track_id = track_info["tracks"]["items"][i]["id"]
            title = track_info["tracks"]["items"][i]["name"]

            #중복 체크
            duplication = self.check_duplication("songs", track_id)
            if duplication > 0:
                #이미 노래가 데이터베이스에 다음 노래로 넘어간다.
                print(f"{title}가 이미 존재합니다.")
                continue

            # songs 테이블에 노래 정보 저장
            artist = track_info["tracks"]["items"][i]["artists"][0]["name"]
            artist_id = track_info["tracks"]["items"][i]["artists"][0]["id"]
            album = track_info["tracks"]["items"][i]["album"]["name"]
            album_id = track_info["tracks"]["items"][i]["album"]["id"]
            relase_date = track_info["tracks"]["items"][i]["album"]["release_date"]
            popularity = track_info["tracks"]["items"][i]["popularity"]
            img640 = track_info["tracks"]["items"][i]["album"]["images"][0]["url"]
            img300 = track_info["tracks"]["items"][i]["album"]["images"][1]["url"]
            img64 = track_info["tracks"]["items"][i]["album"]["images"][2]["url"]

            song_data = (track_id, title, artist, artist_id, album, album_id, relase_date, popularity, img640, img300, img64)
            song_list_data.append(song_data)

            # genre 테이블
            genres = self.get_genre(artist_id)
            for genre in genres :
                duplication = self.check_duplication("genre", genre)
                if duplication <= 0:
                    sql = """INSERT INTO genre (name) VALUES (%s)"""
                    self.cur.execute(sql, genre)
                genre_data = (track_id, genre)
                genre_list_data.append(genre_data)

            # album_image 테이블
            duplication = self.check_duplication("album_image", album_id)
            if duplication > 0:
                #이미 앨범 이미지가 데이터베이스에 존재하면 함수를 종료한다.
                #print(f"{album} 이미지가 이미 존재합니다.")
                print(" ")
            else:
                img640 = track_info["tracks"]["items"][i]["album"]["images"][0]["url"]
                img300 = track_info["tracks"]["items"][i]["album"]["images"][1]["url"]
                img64 = track_info["tracks"]["items"][i]["album"]["images"][2]["url"]

                album_image_data = (album_id, img640, img300, img64)
                album_image_list_data.append(album_image_data)

        print(f"{title}를 추가합니다.")
        return song_list_data, genre_list_data, album_image_list_data
    
    # track_id로 노래 정보를 가져오는 함수
    def get_song_data_from_trakc_id(self, track_id):

        # track_id로 노래 정보 가져오기
        track_info = self.sp.track(track_id)
        title = track_info["name"]
        #중복 체크
        duplication = self.check_duplication("songs", track_id)
        if duplication > 0:
            #이미 노래가 데이터베이스에 다음 노래로 넘어간다.
            print(f"{title}가 이미 존재합니다.")
            return None, None, None
        song_list_data = []
        genre_list_data = []
        album_image_list_data = []

        # songs 테이블
        artist = track_info["artists"][0]["name"]
        artist_id = track_info["artists"][0]["id"]
        album = track_info["album"]["name"]
        album_id = track_info["album"]["id"]
        relase_date = track_info["album"]["release_date"]
        popularity = track_info["popularity"]
        if track_info["album"]["images"] == []:
            img640 = None
            img300 = None
            img64 = None
        else:
            img640 = track_info["album"]["images"][0]["url"]
            img300 = track_info["album"]["images"][1]["url"]
            img64 = track_info["album"]["images"][2]["url"]

        song_data = (track_id, title, artist, artist_id, album, album_id, relase_date, popularity, img640, img300, img64)
        song_list_data.append(song_data)

        # genre 테이블
        genres = self.get_genre(artist_id)

        for genre in genres :
            duplication = self.check_duplication("genre", genre)
            if duplication <= 0:
                sql = """INSERT INTO genre (name) VALUES (%s)"""
                self.cur.execute(sql, genre)
            genre_data = (track_id, genre)
            genre_list_data.append(genre_data)

        # album_image 테이블
        duplication = self.check_duplication("album_image", album_id)
        if duplication > 0:
            #이미 앨범 이미지가 데이터베이스에 존재하면 함수를 종료한다.
            #print(f"{album} 이미지가 이미 존재합니다.")
            print(" ")
        else:
            if track_info["album"]["images"] == []:
                img640 = None
                img300 = None
                img64 = None
            else:
                img640 = track_info["album"]["images"][0]["url"]
                img300 = track_info["album"]["images"][1]["url"]
                img64 = track_info["album"]["images"][2]["url"]
            

            album_image_data = (album_id, img640, img300, img64)
            album_image_list_data.append(album_image_data)
        
        print(f"{title}를 추가합니다.")
        return song_list_data, genre_list_data, album_image_list_data


    # 아티스트의 장르를 가져오는 함수
    def get_genre(self, artist_id):
        artist_info = self.sp.artist(artist_id)
        genre = artist_info["genres"]
        return genre
    

    # 중복 체크 함수
    def check_duplication(self, table, id):
        self.connect_cursor()
        if table == "genre":
            sql = """SELECT COUNT(*) FROM genre WHERE name = %s"""
        elif table == "songs":
            sql = """SELECT COUNT(*) FROM songs WHERE id = %s"""
        elif table == "album_image":
            sql = """SELECT COUNT(*) FROM album_image WHERE id = %s"""
        elif table == "song_status":
            sql = """SELECT COUNT(*) FROM song_status WHERE id = %s"""
        elif table == "artist_songs":
            sql = """SELECT COUNT(*) FROM artist_songs WHERE id = %s"""
        elif table == "spotify_playlist":
            sql = """SELECT COUNT(*) FROM spotify_playlist WHERE id = %s"""

        self.cur.execute(sql, id)
        result = self.cur.fetchone()[0]
        return result
    

    # 데이터베이스에 노래 정보 저장하는 함수
    # title 또는 track_id로 할지 정해야함
    def insert_song_data(self, title=None, track_id=None, limit=1):
        self.connect_cursor()

        # 변수값 가져오기
        if track_id is None:
            song_data_list, genre_list_data, album_image_list_data = self.get_song_data(title, limit=limit)
        else:
            song_data_list, genre_list_data, album_image_list_data = self.get_song_data_from_trakc_id(track_id)
        
        # 결과값들이 이미 있다면 함수를 종료한다.
        if song_data_list is None:
            return None
        
        # 데이터 추가 SQL 쿼리
        song_sql = """INSERT INTO songs (id, title, artist, artist_id, album, album_id, release_date, popularity, 640px, 300px, 64px) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        album_image_sql = """INSERT INTO album_image (id, 640px, 300px, 64px) VALUES (%s, %s, %s, %s)"""
        genre_sql = """INSERT INTO song_genres (song_id, genre) VALUES (%s, %s)"""

        try:
            # SQL 쿼리 실행
            if album_image_list_data is not None:
                # 노래는 없으나, 앨범 이미지는 이미 존재할 때는 실행하지 않는다.
                self.cur.executemany(album_image_sql, album_image_list_data)
            self.cur.executemany(song_sql, song_data_list)
            self.cur.executemany(genre_sql, genre_list_data)

            # 변경 내용을 커밋하여 데이터베이스에 반영
            self.conn.commit()
            
        except Exception as e:
            # 변경 내용 롤백
            self.conn.rollback()
            print('데이터 추가 실패')
            print('에러 메시지:', e)


        return song_data_list

    # track_id로 songs 테이블에 있는 노래의 정보를 보내는 함수
    def send_song_data(self, track_id):
        self.connect_cursor()
        sql = f"SELECT * FROM songs WHERE id = '{track_id}'"
        self.cur.execute(sql)
        song_data = self.cur.fetchall()
        self.close_cursor()
        return song_data
    
    # 빌보드 사이트의 노래 제목을 스포티파이에서의 제목으로 변환
    def billboard_title_to_spotify_title(self, title, artist):
        
        title=title.lower()
        if len(title)>10:
            title=title[:10]
        artist=artist.lower()

        # 최대한 오차를 줄이기 위해 아티스트와 타이틀로 동시 검색
        q=f"remaster%20track:{title}%20artist:{artist}"
        search_type = ("track", "artist")
        track_info = self.sp.search(q=q, limit=1, type=search_type, market='US')


        if track_info["tracks"]["items"] == []:
            #특수문자 검사
            title = str(title)
            title = title.replace('*', 'i')
            track_info = self.sp.search(q=title, type='track', market='US')

        artist_id = track_info["tracks"]["items"][0]["artists"][0]["id"]

        track_id = track_info["tracks"]["items"][0]["id"]
        title = track_info["tracks"]["items"][0]["name"]
        artist = track_info["tracks"]["items"][0]["artists"][0]["name"]
        img640 = track_info["tracks"]["items"][0]["album"]["images"][0]["url"]
        img300 = track_info["tracks"]["items"][0]["album"]["images"][1]["url"]
        img64 = track_info["tracks"]["items"][0]["album"]["images"][2]["url"]
        genres = self.get_genre(artist_id)

        return (track_id, title, artist, img640, img300, img64, genres)
    

    # 노래 스텟을 데이터베이스에 저장하는 함수
    def insert_song_status(self, track_id):
        
        # 중복체크
        duplication = self.check_duplication("song_status", track_id)
        if duplication > 0:
            return 
        
        # 스탯 가져오기
        features = self.sp.audio_features(tracks=[track_id])
        if features[0] == None:
            acousticness = None
            danceability = None
            energy = None
            liveness = None
            loudness = None
            valence = None
            mode = None
            speechiness = None
            instrumentalness = None
            tempo = None
            duration_ms = None
        else:
            acousticness = features[0]["acousticness"]
            danceability = features[0]["danceability"]
            energy = features[0]["energy"]
            liveness = features[0]["liveness"]
            loudness = features[0]["loudness"]
            valence = features[0]["valence"]
            mode = features[0]["mode"]
            speechiness = features[0]["speechiness"]
            instrumentalness = features[0]["instrumentalness"]
            tempo = features[0]["tempo"]
            duration_ms = features[0]["duration_ms"]

        # 저장
        sql = """INSERT INTO SONG_STATUS (id, acousticness, danceability, energy, liveness,
                    loudness, valence, mode, speechiness, instrumentalness, tempo, duration_ms)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cur.execute(sql, (track_id, acousticness, danceability, energy, liveness, loudness,
                               valence, mode, speechiness, instrumentalness, tempo, duration_ms))
        self.conn.commit()
        #print(track_id, ": 스탯 입력 완료")
        
    # songs 테이블 -> song_status 테이블로 데이터 넣는 함수
    def insert_all_status_in_database(self):
        self.connect_cursor()
        sql = "SELECT id FROM songs"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        track_ids = [str(d[0]) for d in data]
        for track_id in track_ids:
            self.insert_song_status(track_id)

    # genre 테이블의 모든 장르를 가져오는 함수
    def get_all_genres(self):
        genre_list = []
        self.connect_cursor()
        sql = "SELECT genre FROM song_genres"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        genre_list = [genre[0] for genre in results]

        return genre_list
    
    # 장르 시각화 함수
    def genre_visualization(self):
        genres = self.get_all_genres()
        genre_count = Counter(genres)
        wordcloud = WordCloud(background_color='white').generate_from_frequencies(genre_count)

        # 시각화
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    # 아티스트의 모든 트랙 목록을 데이터베이스에 저장하는 함수
    def insert_artist_track_list(self, artist_id, artist):
        artist_track_list = []
        self.connect_cursor()
        duplication = self.check_duplication("artist_songs", artist_id)
        print(artist_id)
        if duplication <= 0:
            album_list = set()
            offset = 0
            limit = 50
            while True:
                albums = self.sp.artist_albums(artist_id, country="US", limit=limit, offset=offset)         
                if not albums['items']:
                    break
                
                for album in albums['items']:
                    album_id = album['id']
                    if album_id not in album_list:
                        album_list.add(album_id)


                offset += 1
                print(offset, "|", len(albums['items']))
                
                if offset > 250:
                    break
            #lbums = self.sp.artist_albums(artist_id, country="US", limit=1, offset=0)
            #for album in albums['items']:
            #        album_id = album['id']
            #        if album_id not in album_list:
            #            album_list.add(album_id)
            print(len(album_list))
            album_list = list(album_list)
            album_list.reverse()
            album_list = set(album_list)
            num = 0
            # 앨범 목록 가져오기
            for album_id in album_list:
                #album_id = album['id']
                #album_name = album['name']
                
                # 앨범의 트랙 가져오기
                tracks = self.sp.album_tracks(album_id)
                
                # 트랙 목록 순회
                for track in tracks['items']:
                    is_artist_in = False
                    for artist_info in track['artists']:
                        if artist_info['id'] == artist_id:
                            is_artist_in = True
                            break

                    if is_artist_in == False:
                        print(".")
                        continue

                    if num >= 50:
                        break
                    track_id = track['id']
                    artist_track_list.append(track_id)
                    num = num + 1
                    #노래 정보 없을때 이용
                    self.insert_song_status(track_id)
                    self.insert_song_data(track_id=track_id)
            
            print(len(artist_track_list))
            album_count = len(album_list)
            track_list_text = f"{artist_track_list}"

            sql = """INSERT INTO artist_songs (id, name, songs) VALUES (%s, %s, %s)"""
            self.cur.execute(sql, (artist_id, artist, track_list_text))
            # 변경 내용을 커밋하여 데이터베이스에 반영
            self.conn.commit()


            return artist_track_list

        else:
            return None

    #아티스트의 아이디로 그 아티스트의 트랙 리스트 가져오기
    def get_artist_track_list(self, artist_ids):
        all_track_list = []
        print(artist_ids)
        self.connect_cursor()
        sql = f"SELECT songs FROM artist_songs WHERE id = %s"
        for artist_id in artist_ids:

            self.cur.execute(sql, artist_id)
            songs = self.cur.fetchall()
            
            if songs == ():
                continue
            track_list = ast.literal_eval(songs[0][0])
            
            all_track_list.extend(track_list)

        self.close_cursor()
            
        return all_track_list

    # 아티스트의 모든 트랙 리스트를 가져오는 함수
    # 데이터베이스에 없다면 검색하여 저장하고 보냄
    def get_track_list_from_artist_id(self, artist_ids, artist_list):
        all_track_list = []
        self.connect_cursor()
        num = 50
        if len(artist_ids) < 3:
            num = 100

        for artist_id, artist in zip(artist_ids, artist_list):
            artist_track_list = self.insert_artist_track_list(artist_id, artist)
            if artist_track_list is None:
                sql = f"SELECT songs FROM artist_songs WHERE id = %s"
                self.cur.execute(sql, artist_id)
                songs = self.cur.fetchall()
                #print(songs[0][0])
                track_list = ast.literal_eval(songs[0][0])
                if len(track_list) < num:
                    num = len(track_list)
                track_list = np.random.choice(track_list, num, replace=False)
                print(artist, len(track_list))
                all_track_list.extend(track_list)
            else:
                track_list = np.random.choice(artist_track_list, num, replace=False)
                all_track_list.extend(track_list)

        self.close_cursor()
            
        return all_track_list

    # 키워드로 플레이리스트를 가져오는 함수
    # 장르, 아티스트 외에도 다양하게 검색 가능   
    def get_playlist(self, input_list, num = 2):
        self.connect_cursor()
        playlist_array = []
        for data in input_list:
            # 장르 또는 아티스트 이름 등으로 spotify api에 플레이리스트 검색
            playlist_info = self.sp.search(q=data, type='playlist', market='US', limit=num)
            length = len(playlist_info["playlists"]["items"])

            playlist = []
            for i in range(0, length):
                playlist_id = playlist_info["playlists"]["items"][i]['id']
                playlist_name = playlist_info["playlists"]["items"][i]['name']
                
                # 중복체크
                duplication = self.check_duplication("spotify_playlist", playlist_id)

                #데이터베이스에서 검색된 플레이리스트를 가져옴
                if duplication > 0:
                    playlist_query = f"SELECT * FROM spotify_playlist where id = %s"
                    self.cur.execute(playlist_query, playlist_id)
                    playlist_fetched = self.cur.fetchall()
                    playlist_track_list = ast.literal_eval(playlist_fetched[0][2])
                    playlist_json = {
                        "name": playlist_fetched[0][1],
                        "image": playlist_fetched[0][3],
                        "track_list": playlist_track_list
                    }

                    playlist.append(playlist_json)
                else:
                    print(playlist_name,"가 데이터베이스에 존재하지 않습니다.")

            result = {
                data: playlist
            }

            playlist_array.append(result)
            
        return playlist_array

    # 키워드로 플레이리스트를 저정하는 함수
    # 장르, 아티스트 외에도 다양하게 검색 가능   
    def save_playlist(self, input_list, num = 2):
        self.connect_cursor()

        for data in input_list:
            playlist_info = self.sp.search(q=data, type='playlist', market='US', limit=num)
            length = len(playlist_info["playlists"]["items"])

            for i in range(0, length):
                playlist_track_list = []
                playlist_id = playlist_info["playlists"]["items"][i]['id']
                playlist_name = playlist_info["playlists"]["items"][i]['name']
                
                # 중복체크
                duplication = self.check_duplication("spotify_playlist", playlist_id)
                if duplication > 0:
                    print(playlist_name,"가 이미 있습니다.")
                    continue
                print(playlist_name, "---------------------------------------------------------------------")
                playlist_image = playlist_info["playlists"]["items"][i]['images'][0]['url']
                playlist_track_info = self.sp.playlist_tracks(playlist_id=playlist_id, market='US')
                

                for track in playlist_track_info['items']:
                    if track['track'] is None or track['track']['id'] is None:
                        continue
                    track_id = track['track']['id']
                    self.insert_song_status(track_id)
                    self.insert_song_data(track_id=track_id)
                    playlist_track_list.append(track_id)
                
                track_list_text = f"{playlist_track_list}"
                sql = """INSERT INTO spotify_playlist (id, name, track_list, image) VALUES (%s, %s, %s, %s)"""
                self.cur.execute(sql, (playlist_id, playlist_name, track_list_text, playlist_image))
                # 변경 내용을 커밋하여 데이터베이스에 반영s
                self.conn.commit()

                
            
            
        
        self.close_cursor()
    

    
    # 스포티파이 시간대별 추천을 이용하여 플레이리스트 가져온다.
    def get_featured_playlist(self, month = "08", time = "15"):
        self.connect_cursor()
        day = "00"
        while(day != "31"):
            day = int(day) + 1
            if day < 10:
                day = "0" + str(day)
            else:
                day = str(day)
            timstamp = "2023-" + month + "-" + day + "T"+ time +":00:00"
            print(timstamp)
            print("--------------------------------")
            playlist_info = self.sp.featured_playlists(country='US', limit=5, timestamp=timstamp)
            for playlist in playlist_info['playlists']['items']:
                id = playlist['id']

                # 중복체크
                duplication = self.check_duplication("spotify_playlist", id)
                if duplication > 0:
                    print(playlist['name'],"가 이미 있습니다.")
                    continue

                name = playlist['name']
                image = playlist['images'][0]['url']
                track_list_info = self.sp.playlist(playlist_id=id, market='US')
                track_list = []
                for track in track_list_info['tracks']['items']:
                    track_id = track['track']['id']   
                    self.insert_song_status(track_id)
                    self.insert_song_data(track_id=track_id)
                    track_list.append(track_id)
                track_list_text = f"{track_list}"

                sql = """INSERT INTO spotify_playlist (id, name, track_list, image) VALUES (%s, %s, %s, %s)"""
                self.cur.execute(sql, (id, name, track_list_text, image))
                # 변경 내용을 커밋하여 데이터베이스에 반영s
                self.conn.commit()
        
        self.close_cursor()

#----------------------------------------------------------------------
# 여기 이후 함수들은 데이터베이스에 정보를 저장하거나, 디버깅을 위한 함수
    def get_random_playlist(self, num=50):
        self.connect_cursor()
        sql = f"SELECT id FROM songs"
        self.cur.execute(sql)
        track_list = self.cur.fetchall()
        #print(songs[0][0])
        track_list = [item[0] for item in track_list]
        track_list = np.random.choice(track_list, num, replace=False)
        self.close_cursor()
        return track_list


def to_playlist():
    cur = connect.cursor()
    sql = """SELECT id, name FROM artist ORDER BY popularity DESC"""
    cur.execute(sql)
    artist_list = cur.fetchall()
    for artist in artist_list:
        artist_id = artist[0]
        artist_name = artist[1]
        
        sql = f"SELECT id FROM songs where artist_id = '{artist_id}'"
        
        cur.execute(sql)
        artist_song_list = cur.fetchall()
        artist_song_list = [item[0] for item in artist_song_list]
        
        sql = """SELECT COUNT(*) FROM artist_songs WHERE id = %s"""
        cur.execute(sql, artist_id)
        result = cur.fetchone()[0]
        if result < 1:
            sql = """INSERT INTO artist_songs (id, name, songs) VALUES (%s, %s, %s)"""
            artist_song_list_text = f"{artist_song_list}"
            cur.execute(sql, (artist_id, artist_name, artist_song_list_text))
            print(artist_name, len(artist_song_list), "done")
        connect.commit()

    cur.close()



def get_random_artist_songs():
    seed = int(time.time())
    cur = connect.cursor()
    sql = f"SELECT songs FROM artist_songs ORDER BY RAND({seed}) limit 20"
    cur.execute(sql)
    result = cur.fetchall()
    result = [item[0] for item in result]
    print(len(result))
    all_track_list = []
    for item in result:
        track_list = ast.literal_eval(item)
        all_track_list.extend(track_list)
    
    return all_track_list

def get_random_artist():
    seed = int(time.time())
    cur = connect.cursor()
    sql = f"SELECT name FROM artist ORDER BY RAND({seed}) limit 5"
    cur.execute(sql)
    result = cur.fetchall()
    result = [item[0] for item in result]

    return result

def get_songs_by_genre(genre):
    seed = int(time.time())
    cur = connect.cursor()
    sql = f"SELECT song_id FROM song_genres WHERE genre = '{genre}' ORDER BY RAND({seed}) limit 30"
    cur.execute(sql)
    result = cur.fetchall()
    result = [item[0] for item in result]
    print(result)

    return result

def download1():
    cur = connect.cursor()
    sql = """SELECT id, name FROM artist WHERE popularity < 75 ORDER BY popularity DESC """
    cur.execute(sql)
    artist_list = cur.fetchall()
    for artist in artist_list:
        artist_id = artist[0]
        artist_name = artist[1]
        saf = Spotify_audio_features()
        saf.insert_artist_track_list(artist_id, artist_name)
        
def download2():
    cur = connect.cursor()
    sql = """SELECT name FROM artist WHERE popularity < 79 ORDER BY popularity DESC """
    cur.execute(sql)
    artist_list = cur.fetchall()
    artist_list = [item[0] for item in artist_list]
    sp = Spotify_audio_features()
    sp.save_playlist(artist_list)

def check_artist_track_num():
    cur = connect.cursor()
    sql = """SELECT id, songs, name FROM artist_songs"""
    cur.execute(sql)
    artist_list = cur.fetchall()
    for artist in artist_list:
        artist_id = artist[0]
        track_list = artist[1]
        artist_name = artist[2]
        track_list = ast.literal_eval(track_list)
        length = len(track_list)
        
        if length > 0:
            print(artist_name, length)
            sql = """ DELETE FROM artist_songs WHERE id = %s"""
            cur.execute(sql, artist_id)
        
    connect.commit()
            

def collect_artist_songs():
    cur = connect.cursor()
    sql = """SELECT id, name, popularity FROM artist ORDER BY popularity DESC"""
    cur.execute(sql)
    artist_list = cur.fetchall()
    sp = Spotify_audio_features()
    for artist in artist_list:
        artist_id = artist[0]
        artist_name = artist[1]
        artist_popularity = artist[2]
        duplication = sp.check_duplication("artist_songs", artist_id)
        if duplication > 0:
            continue
        sql = """SELECT id FROM songs where artist_id = %s ORDER BY popularity DESC LIMIT 30"""
        cur.execute(sql, artist_id)
        track_list = cur.fetchall()
        track_list = [item[0] for item in track_list]
        if len(track_list) > 0:
            track_list_text = f"{track_list}"
            print(artist_id, artist_name, track_list_text, len(track_list))
            sql = """INSERT INTO artist_songs (id, name, songs, popularity) VALUES (%s, %s, %s, %s)"""
            cur.execute(sql, (artist_id, artist_name, track_list_text, artist_popularity))
            connect.commit()
        


sp = Spotify_audio_features()
#download2()
#sp.get_random_playlist()