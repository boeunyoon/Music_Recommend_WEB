import React, { useEffect, useState } from 'react'
import SpotifyPlayer from 'react-spotify-web-playback';
const Player = ({ accessToken, trackUri }) => {
    const [play, setPlay] = useState(true)
    useEffect(() => {
        setPlay(true)
    }, [trackUri])
// if(trackUri == null) return null
return (
    <SpotifyPlayer
        token = "BQBBXTKT65WTJjNdynta3Q3rD8LoDHhbJ2Xhw2NrAseEC9qH4nZhRZTOt_MtPTso18BPqZjjujjZBSVVH5rkrX_CgkZ5bwMw4Xe7Ba1QaF9pOm6jxwM"
        showSaveIcon
        callback={state => {
            if(!state.isPlaying) setPlay(false)
        }}
        play = {play}
        uris = "spotify:track:51uoKRa8vT5SULrlF8s2t1"
    />
  )
}

export default Player