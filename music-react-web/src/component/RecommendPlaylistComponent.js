import React, { useEffect, useState } from 'react'
import { Spinner } from 'react-bootstrap';
import { RecommendPlaylistByPlayList } from '../api/musicService';
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import 'react-horizontal-scrolling-menu/dist/styles.css';
import PlaylistCard from './PlaylistCard';
import PlaylistModal from './PlaylistModal';
const RecommendPlaylistComponent = () => {
  const[RecommendPlaylist, setRecommendPlaylist] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null); // 추가: 선택한 플레이리스트 정보 상태

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
  useEffect(()=>{
    RecommendPlaylistByPlayList().then((response) => {
      console.log("RecommendPlaylist",response)
      setRecommendPlaylist(response.data.recommand_playlists);
      setIsLoading(false)
    })
  }, [])
  const clickPlaylist = (playlist, index) => {
      setSelectedPlaylist(playlist)
      console.log("selectedPlaylist",selectedPlaylist)
  }
  if (isLoading) {
    return <Spinner animation="border" variant="light" className='loading'/>
  }
  return (
    <div>
        <ScrollMenu
            onWheel = {onWheel}
        >
            {RecommendPlaylist&&RecommendPlaylist.map((playlist, index) => (
                    <PlaylistCard 
                      playlist={playlist} 
                      key = {index}
                      onClick={() => {
                        clickPlaylist(playlist, index)
                      }}
                    />
            ))}
        </ScrollMenu>
        {selectedPlaylist && (
          <PlaylistModal
            show={selectedPlaylist !== null} // 플레이리스트가 선택되었을 때만 모달을 표시
            playlist={selectedPlaylist}
            onClose={() => setSelectedPlaylist(null)} // 모달을 닫을 때 selectedPlaylist를 null로 설정
          />
        )}
    </div>
  )
}

export default RecommendPlaylistComponent