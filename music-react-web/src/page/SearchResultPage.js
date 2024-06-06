import React, { useState, useEffect, useCallback } from 'react'
import MainLayout from '../layout/MainLayout'
import { useLocation, useNavigate } from 'react-router-dom'
import { searchMusicKeyword } from '../api/musicService';
import { Row, Col } from 'react-bootstrap'
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { BsSearch, BsFillPlusCircleFill } from "react-icons/bs";
import { AiFillHeart,AiOutlineHeart } from "react-icons/ai";
import "../css/page/SearchResultPage.css"
import { AddPlaylist } from '../api/musicService';
import { getplaylist } from '../api/playlistService';
import TrackCard from '../component/TrackCard';
import TrackModal from '../component/Card/TrackModal';
import TrackModalSearch from '../component/Card/TrackModalSearch';
const SearchResultPage = () => {
  const location = useLocation();
  const searchResults = location.state || [];
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInResult, setSearchInResult] = useState(searchResults);
  const [playlist, setPlaylist] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  
  useEffect(() => {
    fetchPlaylist();
  }, []);

  useEffect(() => {
    setSearchInResult(
      searchResults.map(result => ({
        ...result,
        clicked: playlist.some(music => music.songId == result.id),
      }))
    );
  }, [searchResults, playlist]);

  const clickPlaylist = (track) => {
    setSelectedPlaylist(track)
    console.log("selectedPlaylist",selectedPlaylist)
  }

  // 플레이리스트 받아오기
  const fetchPlaylist = () => {
    getplaylist()
      .then(response => {
        setPlaylist(response.data);
        setSearchInResult(
          searchInResult.map(result => ({
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
    const updatedSearchInResult = searchInResult.map(result =>
      result.id === musicId ? { ...result, clicked: !result.clicked } : result
    );

    const playlistContainsMusic = playlist.some(music => music.songId === musicId);

    if (playlistContainsMusic) {
      // 이미 플레이리스트에 있는 경우 제거
      AddPlaylist(music)
        .then(() => {
          setPlaylist(prevPlaylist => prevPlaylist.filter(music => music.songId !== musicId));
          setSearchInResult(updatedSearchInResult);
        })
        .catch(error => {
          console.error('Error removing music from playlist:', error);
        });
    } else {
      // 플레이리스트에 추가
      AddPlaylist(music)
        .then(() => {
          setPlaylist(prevPlaylist => [...prevPlaylist, music]);
          setPlaylist(playlist)
          setSearchInResult(updatedSearchInResult);
        })
        .catch(error => {
          console.error('Error adding music to playlist:', error);
        });
    }
  }, [searchInResult, playlist]);
  useEffect(() => {
    console.log("searchInResult")
    // console.log
  }, [searchInResult]);

  const handleSearch = () => {
    searchMusicKeyword(searchQuery)
      .then(response => {
        const updatedSearchResults = response.data.map(result => ({
          ...result,
          clicked: playlist.some(music => music.id === result.id)
        }));
        setSearchInResult(updatedSearchResults);
        navigate('/search', { state: updatedSearchResults });
      })
      .catch(error => {
        console.error('Error searching music:', error);
      });
  };


  return (
    <MainLayout>
      <h1 className='search-result-title'>검색 결과</h1>
      <InputGroup className="mb-0">
        <Form.Control
          className='search-input'
          placeholder="search"
          aria-label="Recipient's username"
          aria-describedby="basic-addon2"
          value={searchQuery} 
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <Button variant="outline-secondary" id="button-addon2" onClick={handleSearch}>
          <BsSearch className='search-icon'/>
        </Button>
      </InputGroup>
      {searchInResult.length === 0 ? (
        <p>No results found.</p>
      ) : (
        searchInResult.map((result) => (
          <Row 
            key={result.id} 
            className="result-item"
          >
            <Col
            onClick={() => {
              clickPlaylist(result)
            }}
            ><Image src={result.image64} rounded/></Col>
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
        ))
      )}
      {selectedPlaylist && (
              <TrackModalSearch
                show={selectedPlaylist !== null}
                playlist={selectedPlaylist}
                onClose={() => setSelectedPlaylist(null)}
              />
            )}
    </MainLayout>
  )
}

export default SearchResultPage