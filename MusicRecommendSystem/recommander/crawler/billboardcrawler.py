import requests
import pymysql
import sys, os
sys.path.append('./recommander')
sys.path.append('./recommander/crawler')
from spotify import *
from bs4 import BeautifulSoup
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import date
# MySQL 데이터베이스 연결

class Billboard_crawler:
    def __init__(self):
        self.conn = pymysql.connect(
        host='localhost',
        user='root',
        password='950762',
        db='musicanalysis'
        )
        self.cur = self.conn.cursor()

    # 빌보드 사이트에서 날짜를 통해 그 날짜의 빌보드 순위 정보를 크롤링 하는 함수
    def crawling_top_100(self, search_date):
        
        #빌보드 Top 100 데이터 가져오기
        #날짜 타입은 YYYY-MM-DD
        url = 'https://www.billboard.com/charts/hot-100/'

        response = requests.get(f'{url}{search_date}')
        response_html = response.text

        crawling = BeautifulSoup(response_html, 'html.parser')

        #top100 노래 가져오기
        top_100_class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only'
        top_songs = crawling.find_all(name = 'h3', id = 'title-of-a-story', class_ = top_100_class_data)
        top_100 = [song.get_text().strip() for song in top_songs]

        #top1은 top100과 클래스가 다름
        top_1_class_data = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet'
        top_1_song = crawling.find_all(name = 'h3', id = 'title-of-a-story', class_ = top_1_class_data)
        top_1 = [song.get_text().strip() for song in top_1_song]

        top_100.insert(0, top_1[0])

        lastweek_rank_class_data = 'c-label a-font-primary-m lrv-u-padding-tb-050@mobile-max'
        lastweek_rank_data = crawling.find_all('span', class_ = lastweek_rank_class_data)
        lastweek_rank = [song.get_text().strip() for song in lastweek_rank_data]
        sorted_lastweek_rank = []
        length = int(len(lastweek_rank)/6)
        for i in range(0, length):
            sorted_lastweek_rank.append(lastweek_rank[i*6])

        #top1은 top100과 클래스가 다름
        lastweek_top_1_class_data = 'c-label a-font-primary-bold-l a-font-primary-m@mobile-max u-font-weight-normal@mobile-max lrv-u-padding-tb-050@mobile-max u-font-size-32@tablet'
        lastweek_top_1_song = crawling.find_all(name = 'span', class_ = lastweek_top_1_class_data)
        lastweek_top_1 = [song.get_text().strip() for song in lastweek_top_1_song]
        
        sorted_lastweek_rank.insert(0, lastweek_top_1[0])

        #아티스트 이름
        artist_list_class_data = 'c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only'
        artist_list = crawling.find_all(name = 'span', class_ = artist_list_class_data)
        artist_list = [song.get_text().strip() for song in artist_list]

        top_1_artist_class_data = 'c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet'
        top_1_artist = crawling.find_all(name = 'span', class_ = top_1_artist_class_data)
        top_1_artist = [song.get_text().strip() for song in top_1_artist]
        artist_list.insert(0, top_1_artist[0])
        
        print(search_date)
        
        return top_100, sorted_lastweek_rank, artist_list

    # 데이터베이스 내에서 날짜로 중복을 체크
    def check_duplicate(self, date):
        sql = f"SELECT COUNT(*) FROM billboard WHERE billboard_date = '{date}'"
        
        self.cur.execute(sql)
        result = self.cur.fetchone()[0]

        return result

    # 크롤링한 데이터를 데이터베이스에 저장하는 함수
    def insert_billboard_data(self, date):

        duplicate = self.check_duplicate(date)
        if duplicate > 0:
            print("이미 있는 날짜입니다.")
            return
        
        top_100, sorted_lastweek_rank, artist_list = self.crawling_top_100(date)
        
        saf = Spotify_audio_features()
        json_data_list=[]
        for i in range(0, 100):
            get_song_data = saf.billboard_title_to_spotify_title(top_100[i], artist_list[i])
            print(get_song_data)
            song_data = saf.send_song_data(get_song_data[0])
            if song_data == ():
                saf.insert_song_data(track_id=get_song_data[0])
                song_data = saf.send_song_data(get_song_data[0])
            
            json_data = {
                "rank": i+1,
                "track_id": song_data[0][0],
                "title": song_data[0][1],
                "artist": song_data[0][2],
                "image": {
                    "640px": get_song_data[3],
                    "300px": get_song_data[4],
                    "64px": get_song_data[5]
                },
                "genres": get_song_data[6],
                "diffrent_from_last_week": sorted_lastweek_rank[i]
            }
            json_data_list.append(json_data)
        json_data_list_array = f"{json_data_list}"
        
        sql = """INSERT INTO billboard (billboard_date, billboard_data) VALUES (%s, %s)"""
        self.cur.execute(sql, (date, json_data_list_array))
        # 변경 내용을 커밋하여 데이터베이스에 반영
        self.conn.commit()
    
    # insert_billboard_data 함수를 입력된 날짜의 범위만큼 실행하는 함수
    def insert_data_from_range(self, search_date, end_date):
        start_date = search_date
        datetime_search_date = date.fromisoformat(search_date)
        datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
        period = (datetime_end_date - datetime_search_date).days
        if period < 0:
            search_date = end_date
            end_date = start_date
            start_date = search_date
            datetime_search_date = date.fromisoformat(search_date)
            datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
            period = (datetime_end_date - datetime_search_date).days
        while(datetime_search_date!=datetime_end_date):
            self.insert_billboard_data(search_date)
            datetime_search_date += datetime.timedelta(days=1)
            search_date = date.isoformat(datetime_search_date)
        print("크롤링 끝")

    # 데이터베이스에 있는 빌보드 데이터를 가져오는 함수
    def send_data(self, date):
        sql = f"SELECT * FROM billboard WHERE billboard_date = %s"
        self.cur.execute(sql, date)
        billboard_data = self.cur.fetchall()
        billboard_data = ast.literal_eval(billboard_data[0][1])
        return billboard_data
        #return json.dumps(billboard_data[0][1])
    
    # send_data을 범위로서 실행하는 함수
    def send_data_from_range(self, search_date, end_date):
        billboard_range_data = []

        start_date = search_date
        datetime_search_date = date.fromisoformat(search_date)
        datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
        period = (datetime_end_date - datetime_search_date).days
        if period < 0:
            search_date = end_date
            end_date = start_date
            start_date = search_date
            datetime_search_date = date.fromisoformat(search_date)
            datetime_end_date = date.fromisoformat(end_date) + datetime.timedelta(days=1)
            period = (datetime_end_date - datetime_search_date).days
        while(datetime_search_date!=datetime_end_date):
            billboard_data = self.send_data(search_date)
            billboard_range_data.extend(billboard_data)
            datetime_search_date += datetime.timedelta(days=1)
            search_date = date.isoformat(datetime_search_date)

        unique_records = {}
        for record in billboard_range_data:
            if record['track_id'] not in unique_records:
                unique_records[record['track_id']] = record
        

        unique_data = list(unique_records.values())

        return unique_data
    
    # 날짜 범위의 빌보드 데이터에서 장르만을 추출하여 세는 함수
    def get_billboard_genres(self, start_date, end_date):
        data = self.send_data_from_range(start_date, end_date)
        track_id_list = [d['track_id'] for d in data]
        genre_list = []
        for track_id in track_id_list:
            sql = "SELECT genre FROM song_genres WHERE song_id = %s"
            self.cur.execute(sql, (track_id,))
            results = self.cur.fetchall()
            for row in results:
                genre_list.append(row[0])
        
        genre_count = Counter(genre_list)

        return genre_count
    
    # 날짜 범위로 계산된 장르의 수를 센 것을 이미지화하는 함수
    def genre_visualization(self, start_date, end_date):
        genre_count = self.get_billboard_genres(start_date, end_date)
        #genre_count = Counter(genres)
        wordcloud = WordCloud(background_color='white').generate_from_frequencies(genre_count)

        # 시각화
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

