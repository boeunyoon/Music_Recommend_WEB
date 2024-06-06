import React, { useState } from 'react'
import { Card, Image, Col } from 'react-bootstrap';
import "../css/component/SelectGenre.css"

const ArtistCard = ({artist, onSelect}) => {
  const [isSelected, setIsSelected] = useState(false);

  const handleCardClick = () => {
    setIsSelected(!isSelected);
    onSelect(artist);
  };
  return (
    <Col lg={2} md={3} sm={4} xs={6} className="mb-4">
      <Card 
       bg={isSelected ? 'primary' : 'dark'}
       text={isSelected ? 'white' : 'light'}
       onClick={handleCardClick}
       style={{ cursor: 'pointer' }}
      >
        <Image
          src={artist.artistImage}
          alt={artist.artistName}
          roundedCircle
          className="card-img-top card-image"
        />
        <Card.Body>
          <Card.Title>{artist.artistName}</Card.Title>
        </Card.Body>
      </Card>
    </Col>
  )
}

export default ArtistCard