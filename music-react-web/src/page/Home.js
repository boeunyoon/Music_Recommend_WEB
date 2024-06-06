import React, {useState, useEffect, useMemo} from 'react'
import { fetchUserData } from '../api/authenticationService'
import { useNavigate } from 'react-router-dom'
import MainLayout from '../layout/MainLayout'
import "../css/page/Home.css"
import { Row } from 'react-bootstrap'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { BsSearch } from "react-icons/bs";
import { RecommendMusicByPlayList, searchMusicKeyword } from '../api/musicService'
import RecommendByPlaylist from '../component/RecommendByPlaylist'
import RecommendPlaylistComponent from '../component/RecommendPlaylistComponent'
import RecommendPreferComponent from '../component/RecommendPreferComponent'
import Player from '../component/Player/Player'
import RecommendPreferArtistComponent from '../component/RecommendPreferArtistComponent'
const Home = (props) => {
  const [nickname, setNickname] = useState('')
  const navigate = useNavigate();
  const [searchKeyword, setSearchKeyword] = useState('');
  useMemo(()=>{
    fetchUserData().then((response) =>{
      setNickname(response.data.nickname)
      if(response.data.preferenceGenre == null){
        navigate("/select")
      }
    }).catch((err) => {
      if(err.response.status == 401){
        console.log("Authentication Failed")
        navigate("/login")
      }
    })
  },[])
  const hadleSearchbtn=(e)=>{
      e.preventDefault();
      searchMusicKeyword(searchKeyword).then((response)=>{
        navigate("/search", {state: response.data})
      }).catch((err)=>{
        console.error(err);
      })
  }
  const handleInputChange = (event) => {
    setSearchKeyword(event.target.value);
    console.log(searchKeyword);
  };
  console.log("hello", nickname)
  return (
    <>
      {nickname &&
        <MainLayout>
          <Row style={{marginTop:"3%"}}>
            <InputGroup className="mb-0">
              <Form.Control
                className='search-input'
                placeholder="search"
                aria-label="Recipient's username"
                aria-describedby="basic-addon2"
                value={searchKeyword} 
                onChange={handleInputChange}
              />
                <Button variant="outline-secondary" id="button-addon2" 
                  onClick={hadleSearchbtn}
                >
                  <BsSearch className='search-icon'/>
                </Button>
            </InputGroup>
          </Row>
          <Row style={{marginTop:"2%"}}>
            <h2>추천하는 음악</h2>
            <hr style={{size:"10px", color: "white"}}/>
            <RecommendByPlaylist/>
          </Row>
          <Row>
            <h2 style={{marginTop: "10px"}}>추천하는 플레이리스트</h2>
            <hr style={{size:"10px"}}/>
            <RecommendPlaylistComponent/>
          </Row>
          <Row>
            <RecommendPreferComponent/>
          </Row>
          <Row>
            <RecommendPreferArtistComponent/>
          </Row>
        </MainLayout>
      }
    </>
  )
}

export default Home