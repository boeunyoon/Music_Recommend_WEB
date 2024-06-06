import React, { useCallback, useEffect, useState } from 'react'
import { Modal, Button, Image, Row, Col } from 'react-bootstrap'
import { AiFillHeart,AiOutlineHeart } from "react-icons/ai";
import { AddPlaylist, getplaylist } from '../../api/playlistService';
const TrackModal = ({show, playlist, onClose}) => {
    const [currentTrack, setCurrentTrack] = useState(playlist);
    const [myPlaylist, setMyPlaylist] = useState();
    console.log(currentTrack)
    useEffect(() => {
      fetchPlaylist();
    },[])
    const fetchPlaylist = () => {
      getplaylist().then(response => {
        setMyPlaylist(response.data);
        currentTrack(
          currentTrack.map(result => ({
            ...result,
            clicked: response.data.some(music => music.songId == result.id),
          }))
        );
      })
      .catch(error => {
        console.error('Error fetching playlist:', error);
      });
    }
    const handleAddToPlaylist = useCallback((music, musicId) => {
      console.log(music)
      const updatedSearchInResult = currentTrack.map(result =>
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
            setCurrentTrack(updatedSearchInResult);
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
            setCurrentTrack(updatedSearchInResult);
          })
          .catch(error => {
            console.error('Error adding music to playlist:', error);
          });
      }
    }, [myPlaylist, currentTrack]);
    useEffect(() => {
      console.log("currentPlaylist")
      // console.log
    }, [currentTrack]);
    console.log("myPlaylist",myPlaylist)
  return (
    <Modal show={show} onHide={onClose} size="lg" className="modal-container">
      <Modal.Body>
      <Row className = "modal-title">
          <Col><Image src={playlist.image} rounded className = "playlist-image"/></Col>
          <Col>
            <Row>
              <h2>{playlist.title}</h2>
              <h4>{playlist.artist}</h4>
              <h4>release date: {playlist.release_date}</h4>
            </Row>
          </Col>
        </Row>
      </Modal.Body>
      <Modal.Footer>
          {currentTrack.clicked ? (
                <AiFillHeart className="heart-icon" 
                onClick={() => handleAddToPlaylist(currentTrack, currentTrack.id)} />
              ) : (
                <AiOutlineHeart className="heart-icon" 
                onClick={() => handleAddToPlaylist(currentTrack, currentTrack.id)} />
          )}
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </Modal.Footer>
    </Modal>
  )
}

export default TrackModal