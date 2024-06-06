import React, { useEffect, useState, useCallback } from 'react'
import { Modal, Button, Image, Row, Col } from 'react-bootstrap'
import "../css/component/PlaylistModal.css"
import { AddPlaylist, getplaylist } from '../api/playlistService';
import { AiFillHeart,AiOutlineHeart } from "react-icons/ai";

const PlaylistModal = ({ show, playlist, onClose }) => {
  console.log("Selected playlist", playlist);
  const [myPlaylist, setMyPlaylist] = useState([]);
  const [currentPlaylist, setCurrentPlaylist] = useState(playlist.track_list);

  useEffect(() => {
    fetchPlaylist();
  },[])
    // 플레이리스트 받아오기
  const fetchPlaylist = () => {
    getplaylist()
      .then(response => {
        setMyPlaylist(response.data);
        setCurrentPlaylist(
          currentPlaylist.map(result => ({
            ...result,
            clicked: response.data.some(music => music.songId == result.id),
          }))
        );
      })
      .catch(error => {
        console.error('Error fetching playlist:', error);
      });
  };
  const handleAddToPlaylist = useCallback((music, musicId) => {
    console.log(music)
    const updatedSearchInResult = currentPlaylist.map(result =>
      result.id === musicId ? { ...result, clicked: !result.clicked } : result
    );
    console.log("updatedSearchInResult",updatedSearchInResult)

    const playlistContainsMusic = myPlaylist.some(music => music.Id === musicId);
      console.log(playlistContainsMusic)
    if (playlistContainsMusic) {
      // 이미 플레이리스트에 있는 경우 제거
      AddPlaylist(music)
        .then(() => {
          setMyPlaylist(prevPlaylist => prevPlaylist.filter(music => music.Id !== musicId));
          setCurrentPlaylist(updatedSearchInResult);
        })
        .catch(error => {
          console.error('Error removing music from playlist:', error);
        });
    } else {
      // 플레이리스트에 추가
      AddPlaylist(music)
        .then(() => {
          setMyPlaylist(prevPlaylist => [...prevPlaylist, music]);
          setMyPlaylist(myPlaylist)
          setCurrentPlaylist(updatedSearchInResult);
        })
        .catch(error => {
          console.error('Error adding music to playlist:', error);
        });
    }
  }, [myPlaylist, currentPlaylist]);
  useEffect(() => {
    console.log("currentPlaylist")
    // console.log
  }, [currentPlaylist]);
  console.log("myPlaylist",myPlaylist)
  return (
    <Modal show={show} onHide={onClose} size="lg" className="modal-container">
      <Row className = "modal-title">
          <Col><Image src={playlist.image} rounded className = "playlist-image"/></Col>
          <Col><h4>Playlist</h4><br/><h2>{playlist.name}</h2></Col>
      </Row>
      <Row className='title-track'>
          <Col></Col>
          <Col>Title</Col>
          <Col>Artist</Col>
          <Col>Playlist</Col>
      </Row>
      <hr className = "modal-line" style={{backgroundColor: "white"}}/>
      <Modal.Body>
        {currentPlaylist && currentPlaylist.map((result, index) => (
            <Row className = "track-list" key={index}>
              <Col><Image src={result.image64} rounded></Image></Col>
              <Col>{result.title}</Col>
              <Col>{result.artist}</Col>
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
      </Modal.Body>
      <Modal.Footer>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </Modal.Footer>
    </Modal>
  )
}

export default PlaylistModal