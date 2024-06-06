import React, { useEffect, useState, useCallback } from 'react'
import MainLayout from '../layout/MainLayout'
import "../css/page/UserPlaylist.css"
import { AddPlaylist, getUserplaylist } from '../api/playlistService'
import { Col, Row } from 'react-bootstrap'
import Image from 'react-bootstrap/Image';
import { AiFillHeart,AiOutlineHeart } from "react-icons/ai";
const UserPlaylist = () => {
  const [playlist, setPlaylist] = useState([]);
  useEffect(()=>{
    fetchPlaylist()
    // console.log(playlist);
  },[])
  // useEffect(() => {

  // },[playlist]) 
  const fetchPlaylist=()=>{
    getUserplaylist().then((response)=>{
      console.log("response",response.data)
      const update = [...response.data]
      update.forEach((result) => {
          result.clicked = true
      })
      setPlaylist(update)
    }).catch((err)=>{
      console.error(err);
    })
  }

  const handleAddToPlaylist = ((music, musicId) => {
    AddPlaylist(music).then(() => {
      setPlaylist(prevPlaylist => [...prevPlaylist, music]);
      setPlaylist(playlist);
      fetchPlaylist()
    }).catch(error => {
      console.error('Error adding music to playlist:', error);
    })
  });
  console.log("playlist",playlist)
  return (
    <MainLayout>
        <h1 className='playlist-title'>Playlist</h1>
        <hr/>
        {playlist&&playlist.map((result)=>(
            <Row key={result.id} className='playlist-result'
              style={{marginTop: '5px', padding: '5px', alignItems:'center'}}
            >
              <Col><Image src={result.image64} rounded/></Col>
              <Col><p>{result.title}</p></Col>
              <Col><p>{result.artist}</p></Col>
              <Col>
                {result.clicked ? (
                  <AiFillHeart className="heart-icon" 
                  onClick={() => handleAddToPlaylist(result, result.id)} />
                ) : (
                  <AiOutlineHeart className="heart-icon" 
                  onClick={() => handleAddToPlaylist(result, result.id)} />
                )}
            </Col>
            </Row>
        ))}
    </MainLayout>
  )
}

export default UserPlaylist