import React, { useEffect, useState } from 'react'
import { RecommendArtistCon } from '../api/musicService'
import { Spinner } from 'react-bootstrap';
import PreferArtist from './Prefer/PreferArtist';
const RecommendPreferArtistComponent = () => {
    const [RecommendArtist, setRecommendArtist] = useState();
    const [Playlist, setPlaylist] = useState();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        RecommendArtistCon().then((response) => {
            console.log('추천하는 아티스트',response.data);
            setPlaylist(response.data.artist_playlist)
            setRecommendArtist(response.data.top_artist)
            setIsLoading(false)
        })
    }, [])
  if (isLoading) {
    return <div>
        <h2>추천하는 아티스트</h2>
        <hr style={{size:"10px", color: "white"}}/>
        <Spinner animation="border" variant="light" className='loading'/>
    </div>
  }
  return (
    <div>
        {RecommendArtist && RecommendArtist.map((artist, index) =>(
            <PreferArtist
                key={index}
                artist={artist}
                idx={index}
                playlist = {Playlist}
            />
        ))}
    </div>
  )
}

export default RecommendPreferArtistComponent