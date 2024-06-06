import React, { useEffect, useState } from 'react'
import { Spinner } from 'react-bootstrap';
import { RecommendPrefer } from '../api/musicService';
import PreferGenre from './Prefer/PreferGenre';
import "../css/component/RecommendPreferComponent.css"

const RecommendPreferComponent = () => {
  const[RecommendPlaylist, setRecommendPlaylist] = useState();
  const[RecommendArtistPlaylist, setRecommendArtistPlaylist] = useState();
  const[RecommendArtist, setRecommendArtist] = useState();
  const[RecommendGenre, setRecommendGenre] = useState(); //장르 종류 배열
  const[RecommendGenrePlaylist, setRecommendGenrePlaylist] = useState();// 장르별 추천 노래 리스트
  const [isLoading, setIsLoading] = useState(true);
  useEffect(()=>{
    RecommendPrefer().then((response) => {
      console.log("Recommend Prefer Playlist",response.data)
      setRecommendGenrePlaylist(response.data.genre_playlists)
      setRecommendGenre(response.data.top_genre)
      setIsLoading(false)
    })
  }, [])
  if (isLoading) {
    return <div>
      <h2>선호하는 장르</h2>
      <hr style={{size:"10px", color: "white"}}/>
      <Spinner animation="border" variant="light" className='loading'/>
    </div>
  }
  return (
    <div>
      {RecommendGenre && RecommendGenre.map((genre, index) => (
        <PreferGenre
          key={index}
          genre={genre}
          idx={index}
          playlist={RecommendGenrePlaylist}
        />
      ))}
    </div>
  )
}

export default RecommendPreferComponent