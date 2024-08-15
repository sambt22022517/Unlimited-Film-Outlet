import axios from 'axios';
import { useState, useEffect } from 'react';
import MovieList from '../components/MovieList';

// # Formal data
// const data = {
//   tvShows: [
//     { id: 1, title: 'Presumed Innocent', genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', url: '/', ordinal: 1 },
//     { id: 2, title: 'Lady in the Lake', genre: 'Thriller', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', url: '/', ordinal: 2 },
//     { id: 3, title: 'Ted Lasso', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', url: '/', ordinal: 3 },
//     { id: 4, title: 'Time Bandits', genre: 'Adventure', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/jy3YwHfdhEz1jLBZOdePdg/369x208.jpg', url: '/', ordinal: 4 },
//     { id: 5, title: 'Land of Women', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/bAYwyYOKbVDK-JLBqGLLqg/369x208.jpg', url: '/', ordinal: 5 },
//     { id: 6, title: 'Presumed Innocent', genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', url: '/', ordinal: 6 },
//     { id: 7, title: 'Lady in the Lake', genre: 'Thriller', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', url: '/', ordinal: 7 },
//     { id: 8, title: 'Ted Lasso', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', url: '/', ordinal: 8 },
//     { id: 9, title: 'Time Bandits', genre: 'Adventure', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/jy3YwHfdhEz1jLBZOdePdg/369x208.jpg', url: '/', ordinal: 9 },
//     { id: 10, title: 'Land of Women', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/bAYwyYOKbVDK-JLBqGLLqg/369x208.jpg', url: '/', ordinal: 10 }
//   ],
//   movies: [
//     { id: 1, title: 'The Family Plan', year: 2023, genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/tPJwMGtsAr_psAVlyf2Rzg/369x208.jpg', url: '/', ordinal: 1 },
//     { id: 2, title: 'Ghosted', year: 2023, genre: 'Action', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/Ze8uZ-TWJ2JMbqmtcz8_BA/369x208.jpg', url: '/', ordinal: 2 },
//     { id: 3, title: 'Luck', year: 2022, genre: 'Animation', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/gHMoyFnOUJLH6d0rSgyIbg/369x208.jpg', url: '/', ordinal: 3 },
//     { id: 4, title: 'Argylle', year: 2024, genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/i5y5PDuv51g6bV48moKF_Q/369x208.jpg', url: '/', ordinal: 4 },
//     { id: 5, title: 'Killers of the Flower Moon', year: 2023, genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/rss8pF-klNy76S-NWFue-A/369x208.jpg', url: '/', ordinal: 5 }, 
//     { id: 6, title: 'The Family Plan', year: 2023, genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/tPJwMGtsAr_psAVlyf2Rzg/369x208.jpg', url: '/', ordinal: 6 },
//     { id: 7, title: 'Ghosted', year: 2023, genre: 'Action', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/Ze8uZ-TWJ2JMbqmtcz8_BA/369x208.jpg', url: '/', ordinal: 7 },
//     { id: 8, title: 'Luck', year: 2022, genre: 'Animation', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/gHMoyFnOUJLH6d0rSgyIbg/369x208.jpg', url: '/', ordinal: 8 },
//     { id: 9, title: 'Argylle', year: 2024, genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/i5y5PDuv51g6bV48moKF_Q/369x208.jpg', url: '/', ordinal: 9 },
//     { id: 10, title: 'Killers of the Flower Moon', year: 2023, genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/rss8pF-klNy76S-NWFue-A/369x208.jpg', url: '/', ordinal: 10 }
//   ]
// };

function Home() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  // Fetch data from the server after loging in (with credentials) (comment this block of code when testing without loging in)
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await axios.get('http://localhost:8000/api/data', { withCredentials: true });
  //       setData(response.data);
  //     } catch (err) {
  //       setError('Failed to fetch data.');
  //       console.error('Error:', err);
  //     }
  //   };

  //   fetchData();
  // }, []);

  // Fetch data from the server without loging in
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000');
        setData(response.data);
      } catch (err) {
        setError('Failed to fetch data.');
        console.error('Error:', err);
      }
    };

    fetchData();
  }, []);

  if (!data) {
    return (
      <div>
        <p>Loading... Please start the server to fetch data</p>
        <h1>Nhắn tin cho t để fix nếu chạy bị lỗi</h1>
      </div>
    )
  }

  return (
    <div className='vl'>
      {error && <p>{error}</p>}
      <MovieList title='TV Shows' items={data.tvShows} />
      <div className="divider"></div>
      <MovieList title='Movies' items={data.movies} />
      <div className="divider"></div>
      <MovieList title='Movies' items={data.movies} />
      <div className="divider"></div>
      <MovieList title='Movies' items={data.movies} />
    </div>
  );
}

export default Home;