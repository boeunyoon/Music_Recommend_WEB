import React, { useEffect, useState } from 'react'
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import { Row } from 'react-bootstrap'
import PlaylistModal from '../PlaylistModal'
import 'react-horizontal-scrolling-menu/dist/styles.css';
import PreferArtistCard from './PreferArtistCard';
const PreferArtist = (props) => {
  const [selectPlayList, setSelectPlayList] = useState();
  const [selectedPlaylist, setSelectedPlaylist] = useState(null); // 추가: 선택한 플레이리스트 정보 상태
  const ArtistName = props.artist.toUpperCase()
  useEffect(() => {
    setSelectPlayList(props.playlist[props.idx][props.artist])
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
      <h2>추천하는 아티스트 - {ArtistName}</h2>
      <hr/>
      <ScrollMenu
        onWheel={onWheel}
      >
      {selectPlayList && selectPlayList.map((track, index) => (
        <PreferArtistCard
          key={index}
          trackInfo={track}
          onClick={() => {
            clickPlaylist(track, index)
          }}
        />
      ))}
      </ScrollMenu>
      {selectedPlaylist && (
        <PlaylistModal
          show={selectedPlaylist != null}
          playlist={selectedPlaylist}
          onClose={() => setSelectedPlaylist(null)}
        />
      )}
    </Row>
  )
}

export default PreferArtist