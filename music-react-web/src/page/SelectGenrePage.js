import React, { useEffect, useState } from 'react'
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { BsSearch } from "react-icons/bs";
import Button from 'react-bootstrap/Button';
import { Col, Row } from 'react-bootstrap'
import { getAllArtistList, sendArtistList } from '../api/musicService';
import { useNavigate } from 'react-router-dom';
import ArtistCard from '../component/ArtistCard';
import {Container } from 'react-bootstrap';
import "../css/component/SelectGenre.css"
const SelectGenrePage = () => {

  const [selectedArtist, setSelectedArtist] = useState(null);
  const [selectedArtists, setSelectedArtists] = useState([]);
  const [artistList, setArtistList] = useState();
  const navigate =  useNavigate();
  useEffect(()=>{
    getAllArtistList().then((response) =>{
      console.log(response.data.artist_info)
      setArtistList(response.data.artist_info)
    }).catch((err)=>{
      if(err){
        navigate("/")
      }
    })
  },[])
  const handleArtistSelect = (artist) => {
    if (selectedArtists.includes(artist)) {
      setSelectedArtists(selectedArtists.filter((selectedArtist) => selectedArtist !== artist));
      console.log(selectedArtists)
    } else {
      setSelectedArtists([...selectedArtists, artist]);
      console.log(selectedArtists)
    }
  };
  const handleArtistList = () => {
    if (selectedArtists.length < 5){
      alert("5개 이상 아티스트를 선택 하세요")
    }else{
      console.log(selectedArtists)
      sendArtistList(selectedArtists).then((response) => {
        navigate("/")
      }).catch((err) => {
        if(err){
          alert(err)
        }
      })
    }
  }

  return (
    <div style={{marginTop:'30px'}}>
      {artistList &&
        <div className='wrapper-list'>
        <Row className='title-wrapper'>
          <Col lg={4} md={4} sm={4} xs={6}>
            <h2>선호하는 아티스트를 선택하세요</h2>
          </Col>
          <Col lg={1} md={2} sm={2} xs={3}>
            <button 
              className='send-btn'
              onClick={handleArtistList}
            >선택완료</button>
          </Col>
        </Row>
        <Row style={{marginTop:"3%", marginBottom:"3%"}}>
            <InputGroup className="mb-0">
              <Form.Control
                className='search-input'
                placeholder="search"
                aria-label="Recipient's username"
                aria-describedby="basic-addon2"
              />
              <Button variant="outline-secondary" id="button-addon2">
                <BsSearch className='search-icon'/>
              </Button>
            </InputGroup>
        </Row>
        <Container>
          <Row>
            {artistList&&artistList.map((artist) => (
              <ArtistCard 
                key={artist.artistId} 
                artist={artist} 
                onSelect = {handleArtistSelect}
              />
            ))}
          </Row>
        </Container>

    </div>
      }
    </div>
  )
}

export default SelectGenrePage