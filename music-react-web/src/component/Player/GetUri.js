import axios from 'axios';
export const getUri = async(trackId, accessToken) => {
    try {
        const response = await axios.get(`https://api.spotify.com/v1/tracks/${trackId}`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
  
        const { uri } = response.data;
        return uri
      } catch (error) {
        console.error('Error getting track URI:', error);
      }
}