import React, { useState } from 'react'
import { Card } from 'react-bootstrap'
import logo from '../component/image/Spotify_icon.png'
const PlaylistCard = (props) => {
  const [onError, setOnError] = useState(false)
  const handleErrorImage = () => {
    setOnError(true)
  }
  return (
    <div>
        <Card style={{ width: '15rem', backgroundColor: '#282c34', height: '385px', marginLeft:'10px' }}
          onClick={() => props.onClick()}
        >
          {onError ? (
            <Card.Img variant="top" src={logo}/>
          ):(
            <Card.Img variant="top" src={props.playlist.image} onError={handleErrorImage}/>
          )}
          <Card.Body>
            <Card.Title>{props.playlist.name}</Card.Title>
          </Card.Body>
        </Card>
    </div>
  )
}

export default PlaylistCard