import React, {useState, useEffect, useMemo} from 'react'
import '../css/component/SideBar.css'
import { fetchUserData } from '../api/authenticationService'
import Image from 'react-bootstrap/Image'
import {FaUserCircle} from "react-icons/fa";
import {BsFillPersonFill, BsMusicPlayerFill, BsMusicNoteList, BsFillHouseFill} from "react-icons/bs";
import { useNavigate } from 'react-router-dom'
import { logoutActionHandler } from '../api/authenticationService';
const SideBar = (props) => {
  const [nickname, setNickname] = useState('')
  const navigate = useNavigate();
  useMemo(()=>{
    fetchUserData().then((response) =>{
      console.log("response", response);
      setNickname(response.data.nickname)
    }).catch((err) => {
      if(err.response.status == 401){
        console.log("Authentication Failed")
        navigate("/login")
      }
    })
  },[])
  const handleLogout =()=> {
      logoutActionHandler();
      navigate("/login");
  }
  const clickProfile=()=>{
    navigate("/profile");
  }
  const clickTop100=()=>{
    navigate("/top100");
  }
  const clickHome=()=>{
    navigate("/")
  }
  const clickPlaylist=()=>{
    navigate("/playlist")
  }
  return (
    <div>
      <div className='sidebar-iteam-userprofile' >
        <FaUserCircle className='user-icon' size={100}/>
      </div>
      <div className='sidebar-iteam'>
        Welcome {nickname}
      </div>
      <div className='sidebar-iteam' onClick={clickHome}>
        <BsFillHouseFill size={25} className="iteam-icon"/>
        Home
      </div>
      <div className='sidebar-iteam' onClick={clickPlaylist}>
        <BsMusicPlayerFill size={25} className="iteam-icon"/>
        My playList
      </div>
      <div className='sidebar-iteam' onClick={clickProfile}>
        <BsFillPersonFill size={25} className="iteam-icon"/>
        Profile
      </div>
      <div className='sidebar-iteam' onClick={clickTop100}>
        <BsMusicNoteList size={25} className="iteam-icon"/>
        Top 100
      </div>
      <div className='sidebar-btn'>
        <button 
          className='logout-btn'
          onClick={handleLogout}
        >Logout</button>
      </div>
    </div>
  )
}

export default SideBar