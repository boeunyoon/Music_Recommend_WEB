import React, { useEffect, useState } from 'react'
import { RecommendMusicByPlayList } from '../api/musicService';
import '../css/component/RecommendByPlaylist.css'
import { Spinner } from 'react-bootstrap';
import TrackCard from './TrackCard';
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import 'react-horizontal-scrolling-menu/dist/styles.css';
import TrackModal from './Card/TrackModal';

const RecommendByPlaylist = () => {
    const [RecommendMusic, setRecommendMusic] = useState();
    const [isLoading, setIsLoading] = useState(true);
    const [selectedPlaylist, setSelectedPlaylist] = useState(null);
    //마우스 휠로 스크롤 하기
    function onWheel(apiObj, ev){
        const isThouchpad = Math.abs(ev.deltaX) !== 0 || Math.abs(ev.deltaY) < 15;

          if (isThouchpad) {
            ev.stopPropagation();
            return;
          }

          if (ev.deltaY > 0) {
            apiObj.scrollNext();
          } else if (ev.deltaY < 0) {
            apiObj.scrollPrev();
          }
    }

    const clickPlaylist = (track, index) => {
      setSelectedPlaylist(track)
      console.log("selectedPlaylist",selectedPlaylist)
    }

    useEffect(()=>{
        RecommendMusicByPlayList().then((response) => {
            console.log("RecommendMusic",response)
            // Assume the response is an object with a "music" property containing an array of music data
            setRecommendMusic(response.data.recommand_songs); // Extract the array from the response object
            setIsLoading(false);
        })
    },[])
    
    if (isLoading) {
        return <Spinner animation="border" variant="light" className='loading'/>
    }
    return (
        <div>
            <ScrollMenu
                onWheel = {onWheel}
            >
                {RecommendMusic&&RecommendMusic.map((music, index) => (
                        <TrackCard 
                          music={music} 
                          key = {index}
                          onClick={() => {
                            clickPlaylist(music, index)
                          }}
                        />
                ))}
            </ScrollMenu>
            {selectedPlaylist && (
              <TrackModal
                show={selectedPlaylist !== null}
                playlist={selectedPlaylist}
                onClose={() => setSelectedPlaylist(null)}
              />
            )}
        </div>
  )
}

export default RecommendByPlaylist