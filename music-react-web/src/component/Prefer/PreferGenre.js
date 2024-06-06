import React, { useEffect, useState } from 'react'
import { Row } from 'react-bootstrap'
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import 'react-horizontal-scrolling-menu/dist/styles.css';
import PreferGenreCard from './PreferGenreCard';
import PlaylistModal from '../PlaylistModal'
const PreferGenre = (props) => {
  const [selectPlayList, setSelectPlayList] = useState();
  const [selectedPlaylist, setSelectedPlaylist] = useState(null); // 추가: 선택한 플레이리스트 정보 상태
  const GenreName = props.genre.toUpperCase()
  useEffect(() => {
    setSelectPlayList(props.playlist[props.idx][props.genre])
  }, [])
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
  const clickPlaylist = (playlist, index) => {
    setSelectedPlaylist(playlist)
    console.log("selectedPlaylist",selectedPlaylist)
  }
  return (
    <Row style={{marginTop:"2%"}}>
        <h2>선호하는 장르 - {GenreName}</h2>
        <hr/>
        <ScrollMenu
          onWheel={onWheel}
        >
          {selectPlayList && selectPlayList.map((track, index) => (
            <PreferGenreCard
              key={index}
              trackInfo = {track}
              onClick={() => {
                clickPlaylist(track, index)
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
    </Row>
  )
}

export default PreferGenre