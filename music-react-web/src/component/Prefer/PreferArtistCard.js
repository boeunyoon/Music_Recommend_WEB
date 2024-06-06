import React, { useState } from 'react'
import { Card, Button } from 'react-bootstrap'
import logo from '../image/Spotify_icon.png'
const PreferArtistCard = (props) => {
  const [onError, setOnError] = useState(false)
  const handleErrorImage = () => {
    setOnError(true)
  }
  return (
    <div>
      <Card style={{ width: '15rem', backgroundColor: '#282c34', height: '385px', marginLeft:'10px'}}
        onClick={() => props.onClick()}
      >
        {onError ? (
          <Card.Img variant="top" src={logo}/>
        ):(
          <Card.Img variant="top" src={props.trackInfo.image} onError={handleErrorImage}/>
        )}
        <Card.Body>
          <Card.Title>{props.trackInfo.name}</Card.Title>
        </Card.Body>
      </Card>
    </div>
  )
}

export default PreferArtistCard