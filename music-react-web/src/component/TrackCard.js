import React from 'react'
import { Card } from 'react-bootstrap'
const TrackCard = (props) => {
  return (
    <div>
        <Card style={{ width: '15rem', backgroundColor: '#282c34', height: '385px', marginLeft:'10px' }}
          onClick={() => props.onClick()}
        >
          <Card.Img variant="top" src={props.music.image} />
          <Card.Body>
            <Card.Title>{props.music.title}</Card.Title>
            <Card.Text>
              {props.music.artist}
            </Card.Text>
          </Card.Body>
        </Card>
    </div>
  )
}

export default TrackCard