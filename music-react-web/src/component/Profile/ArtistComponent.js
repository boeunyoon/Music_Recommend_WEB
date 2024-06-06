import React from 'react'
import { Card, Button, Image, Col } from 'react-bootstrap'
import '../../css/component/ArtistComponent.css'
const ArtistComponent = (props) => {
  return (
    <Card style={{ 
        width: '15rem', 
        backgroundColor: 'black', 
        marginLeft:'10px', 
        padding:'15px' }}
    >
        <Image 
            className="card-img-top card-image" 
            src={props.artist.image} 
            roundedCircle 
        />
        <Card.Title className='artist-name'>{props.artist.name}</Card.Title>
    </Card>
  )
}

export default ArtistComponent