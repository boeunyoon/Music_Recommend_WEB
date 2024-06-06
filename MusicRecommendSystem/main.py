import sys, os
sys.path.append('./recommander')
sys.path.append('./recommander/crawler')
from fastapi import FastAPI
from pydantic import BaseModel
from recommander.crawler.billboardcrawler import *
from recommander.crawler.spotify import *
from recommander.recommand import *
from recommander.dbconnect import *
import collections
app = FastAPI()

# 유저 형식
class User(BaseModel):
    name: str
    nickname: str

# 데이터 형식
class DataInput(BaseModel):
    user_info: User
    input: dict

#Spotify 권한
#cid = '01b9ce28405042deb84a4813e63d557d'
#secret = 'd20308c58757497191c1386264672528'

#cid = '133e17352a85443a803690b5adaff2c4'
#secret = 'e1bf131abfce43999e5ff0df91ac388a'

cid = '5b7c904f46af4291ada0ec351594ec00'
secret = 'b3f3f4f7e77e4f67bc258331e0465d76'

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 추천 결과값 보내기
@app.post("/recommand")
async def recommand(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)

    # 추천 시스템
    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}}
    # {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    if key == "track_list":
        access_token = get_access_token(cid, secret)

        track_list = data.input['track_list']
        
        length = 30
        
        
        recommand_songs = recommand_from_tracklist(track_list, length)
        result = {
            "access_token": access_token,
            "recommand_songs": recommand_songs
        }
        
        return result
    
    else:
          print("유효하지 않은 데이터 형식입니다.")

# 첫 화면
@app.post("/first_select")
async def first_select(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)

    #첫 화면 아티스트 선택
    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"artist_list": ["Taylor Swift", "The Weeknd", "Drake", "Lana Del Rey", "Ed Sheeran"]}}
    # {"artist_list": ["Taylor Swift", "The Weeknd", "Drake", "Lana Del Rey", "Ed Sheeran"]}
    if key == "artist_list":
        access_token = get_access_token(cid, secret)

        artist_list = data.input['artist_list']
        artist_id_list = get_artist_id(artist_list)
        

        sp = Spotify_audio_features()
        track_list = sp.get_artist_track_list(artist_id_list)
        num = 50
        if len(track_list) <= num:
            num = len(track_list) - 1
        print(num)
        recommand_songs = recommand_from_tracklist(track_list, num)

        recommand_playlists = compare_playlists(track_list)

        top_genre = get_top3_genres_from_track_list(track_list)
        genre_playlist = sp.get_playlist(top_genre)

        result ={
            "access_token": access_token,
            "recommand_songs": recommand_songs,
            "recommand_playlists": recommand_playlists,
            "genre_playlists": {
                "top_genre": top_genre,
                "playlists": genre_playlist
            }
        }

        return result

    else:
          print("유효하지 않은 데이터 형식입니다.")


# 좋아하는 아티스트 가져오기---------
@app.post("/prefer_artist")
async def prefer_artist(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)

    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    # {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    if key == "track_list":
        access_token = get_access_token(cid, secret)

        track_list = data.input['track_list']
        top_artist = get_artist_count(track_list)
        print(top_artist)
        artist_playlist = sp.get_playlist(top_artist)
        result = {
            "access_token": access_token,
            "top_artist": top_artist,
            "artist_playlist": artist_playlist
        }
        
        return result

    else:
          print("유효하지 않은 데이터 형식입니다.")

# 좋아하는 장르 가져오기---------
@app.post("/prefer_genre")
async def prefer_genre(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)

    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    # {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    if key == "track_list":
        access_token = get_access_token(cid, secret)

        track_list = data.input['track_list']
        top_genre = get_top3_genres_from_track_list(track_list)
        genre_playlist = sp.get_playlist(top_genre)
        result = {
            "access_token": access_token,
            "top_genre": top_genre,
            "genre_playlists": genre_playlist
        }
        
        return result

    else:
          print("유효하지 않은 데이터 형식입니다.")

def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text,"%Y-%m-%d")
		return True
	except ValueError:
		return False

# 플레이리스트 추천 결과 보내기
@app.post("/playlist_recommand")
async def playlist_recommand(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)
    
    # 플레이리스트 추천 시스템
    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}}
    # {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    if key == "track_list":
        access_token = get_access_token(cid, secret)
        track_list = data.input['track_list']
        start = time.time()
        recommand_playlists = compare_playlists(track_list)
        
        result = {
            "access_token": access_token,
            "recommand_playlists": recommand_playlists
        }
        end = time.time()
        print(f"{end - start:.5f} sec")
        return result
    
    else:
          print("유효하지 않은 데이터 형식입니다.")

# 아티스트 추천
@app.post("/artist_recommand")
async def artist_recommand(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)
    
    # 플레이리스트 추천 시스템
    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["0yLdNVWF3Srea0uzk55zFn", "7x9aauaA9cu6tyfpHnqDLo", "3k79jB4aGmMDUQzEwa46Rz", "7ABLbnD53cQK00mhcaOUVG"]}}
    # { "track_list": ["0yLdNVWF3Srea0uzk55zFn", "7x9aauaA9cu6tyfpHnqDLo", "3k79jB4aGmMDUQzEwa46Rz", "7ABLbnD53cQK00mhcaOUVG"]}
    if key == "track_list":
        access_token = get_access_token(cid, secret)

        track_list = data.input['track_list']
        top_artist = compare_artists(track_list, 3)
        artist_playlist = sp.get_playlist(top_artist)
        
        result = {
            "access_token": access_token,
            "top_artist": top_artist,
            "artist_playlist": artist_playlist
        }
        return result
    
    else:
          print("유효하지 않은 데이터 형식입니다.")

# 프로필 정보
@app.post("/profile")
async def profile_information(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)
    # { "user_info": { "name": "string", "nickname": "string"}, "input": {"track_list": ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]}
    # {"track_list": ["0yLdNVWF3Srea0uzk55zFn", "7x9aauaA9cu6tyfpHnqDLo", "3k79jB4aGmMDUQzEwa46Rz", "7ABLbnD53cQK00mhcaOUVG"]}
    
    if key == "track_list":
        access_token = get_access_token(cid, secret)

        track_list = data.input['track_list']
        genre_count = get_songs_genres_count(track_list)
        genre_count = dict(genre_count)

        prefer_artists = get_songs_artist_count(track_list)

        result = {
            "access_token": access_token,
            "genres_count": genre_count,
            "prefer_artist": prefer_artists
        }

        return result

# 테스트 전용
@app.post("/test")
async def test(data: DataInput):
    key = next(iter(data.input.keys()))
    print(key)
    start = time.time()
    sp = Spotify_audio_features()
    #while(1):
    #    track_list = get_random_artist_songs()
    #    top_genre = get_top3_genres_from_track_list(track_list)
    #    sp.save_playlist(top_genre)
    #track_list = sp.get_random_playlist()
    #recommand_songs = recommand_from_tracklist(track_list, 5)
    track_list = ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]
    track_list = get_songs_by_genre("rap")
    
    a = recommand_from_tracklist(track_list, len(track_list))
    result = {
       "a":a  
    }
    end = time.time()

    print(f"{end - start:.5f} sec")
    
    return result


# 액세스 토큰
def get_access_token(client_id, client_secret):
    endpoint = 'https://accounts.spotify.com/api/token'

    encoded = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('ascii')

    headers = {'Authorization': f'Basic {encoded}'}
    payload = {'grant_type': 'client_credentials'}

    response = requests.post(endpoint, data=payload, headers=headers)
    # print(json.loads(response.text))
    access_token = json.loads(response.text)['access_token']

    return access_token

# 아티스트 리스트 -> 아티스트 아이디 리스트
def get_artist_id(artist_list, boolean = True):
    cur = connect.cursor()
    
    query = "SELECT id FROM artist WHERE name = %s"
    if boolean == True:
        params = [(name,) for name in artist_list]
    else:
        params = artist_list
    artist_ids = []

    for param in params:
        cur.execute(query, param)
        result = cur.fetchone()
        artist_id = result[0] if result else None
        if artist_id is not None:
            artist_ids.append(artist_id)

    return artist_ids


     

# top3 아티스트
def get_artist_count(track_list):
    cur = connect.cursor()

    query = "SELECT artist FROM songs WHERE id = %s"
    params = [(id,) for id in track_list]

    artists = []

    for param in params:
        cur.execute(query, param)
        result = cur.fetchone()
        artist = result[0] if result else None
        artists.append(artist)

    artist_count = Counter(artists)
    artist_count.pop(None, None)
    print(artist_count)
    top_artist = [artist for artist, count in artist_count.most_common(3)]
    
    return top_artist

# 아티스트 이름으로 아티스트 추천
def get_artist_recommand(artist_list, boolean = True):
    artist_id_list = get_artist_id(artist_list, boolean)
    artist_track_list = sp.get_artist_track_list(artist_id_list)
       
    recommand_artist = compare_artists(artist_track_list)

    return recommand_artist

sp = Spotify_audio_features()

#artist_list = ["one way", "Audio Adrenaline", "Maroon 5"]
track_list = ["3MnewZrZDqej6thgEx3OB1", "3OHfY25tqY28d16oZczHc8", "6AQbmUe0Qwf5PZnt4HmTXv", "2dHHgzDwk4BJdRwy9uXhTO"]
#sp.get_playlist(artist_list)
#track_list = sp.get_track_list_from_artist_id(get_artist_id(artist_list), artist_list)
#result = recommand_from_tracklist(track_list, 3)
#sp.get_featured_playlist(month="07", time="16")
#get_artist_count(track_list)


