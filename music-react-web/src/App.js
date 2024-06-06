import logo from './logo.svg';
import { HashRouter, Routes, Route, Switch, BrowserRouter, useNavigate } from 'react-router-dom';
import './App.css';
import Login from './page/Login';
import Home from './page/Home';
import SignUp from './page/SignUp';
import Profile from './page/Profile';
import Top100 from './page/Top100';
import MainLayout from './layout/MainLayout';
import SelectGenrePage from './page/SelectGenrePage';
import SearchResultPage from './page/SearchResultPage';
import UserPlaylist from './page/UserPlaylist';
import { useEffect } from 'react';
function App() {
  return (
    <BrowserRouter>
      <div className='App-header'>
        <Routes>
          <Route path="/login" element={<Login/>} />
          <Route path="/signup" element={<SignUp/>} />
          <Route path="/" element={<Home/>} />
          <Route path='/profile' element={<Profile/>}/>
          <Route path='/top100' element={<Top100/>}/>
          <Route path='/select' element={<SelectGenrePage/>}/>
          <Route path='/search' element={<SearchResultPage/>}/>
          <Route path='/playlist' element={<UserPlaylist/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
