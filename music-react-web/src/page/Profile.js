import React, { useEffect, useState } from 'react'
import MainLayout from '../layout/MainLayout'
import "../css/page/Profile.css"
import { getProfileData } from '../api/authenticationService'
import GenreComponent from '../component/Profile/GenreComponent'
import ArtistComponent from '../component/Profile/ArtistComponent'
import { Col, Row } from 'react-bootstrap'
const Profile = () => {
  const [genre, setGenre] = useState()
  const [genreName, setGenreName] = useState([])
  const [genreCount, setGenreCount] = useState([])
  const [artist, setArtist] = useState()
  useEffect(() => {
    getProfileData().then((response) =>{
      if (response.data) {
        console.log(response.data);
        const genreNames = Object.keys(response.data.genres_count);
        const genreCounts = Object.values(response.data.genres_count);
        setGenreName(genreNames);
        setGenreCount(genreCounts);
        setArtist(response.data.prefer_artist);
      }
    })

  }, [])
  return (
    <MainLayout>
        <h1 className='title-profile'>Profile</h1>
        <hr/>
        <h2>선호하는 장르</h2>
        {genreCount && genreName && 
          <GenreComponent genreCount = {genreCount} genreName = {genreName}/>
        }
        <h2>선호하는 아티스트</h2>
        <hr/>
        <Row className='background-artist' xl={4}>
          {artist && artist.map((ar, index) => (
            <Col>
              <ArtistComponent artist = {ar} key = {index}/>
            </Col>
          ))}
        </Row>
    </MainLayout>
  )
}

export default Profile