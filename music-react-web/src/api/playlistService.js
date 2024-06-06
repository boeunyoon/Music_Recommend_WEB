import axios from 'axios';
const getToken=()=>{
    return localStorage.getItem("USER_KEY")
}

//플레이리스트 추가하기
export const AddPlaylist=(keyword)=>{
    console.log(keyword);
    return axios({
        method:'POST',
        url: `${process.env.hostUrl||'http://localhost:8080'}/addplaylist`,
        headers:{
            'Content-Type': 'application/json',
            'Authorization':'Bearer '+getToken()
        },
        data: JSON.stringify(keyword)
    })
}

//플레이리스트 조회
export const getplaylist=()=>{
    return axios({
        method:'GET',
        url: `${process.env.hostUrl||'http://localhost:8080'}/getplaylist`,
        headers:{
            'Authorization':'Bearer '+getToken()
        },
    })
}
///playlist에 들어가는 api
export const getUserplaylist=()=>{
    return axios({
        method:'GET',
        url: `${process.env.hostUrl||'http://localhost:8080'}/playlist`,
        headers:{
            'Authorization':'Bearer '+getToken()
        },
    })
}