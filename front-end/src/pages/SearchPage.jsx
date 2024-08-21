import { useContext, useEffect, useState } from "react";
import MovieItem from "../components/MovieItem";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";
import '../styles/Search.css';
// import { fetchSearchResults } from "../api";

function SearchPage() {
  const { searchQuery } = useContext(AuthContext);

  const [filters, setFilters] = useState({
    q: '',
    genre: [],
    price: { min: '', max: '' },
    rating: [],
  });

  const [searchResults, setSearchResults] = useState([
    { id: 1, title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', rating: 4, genre: 'Thriller', year: 1990 },
    { id: 2, title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', rating: 3, genre: 'Mystery', year: 1947 },
    { id: 3, title: 'Ted Lasso', price: 9.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', rating: 5, genre: 'Comedy', year: 2020 },
    { id: 4, title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', rating: 4, genre: 'Thriller', year: 1990 },
    { id: 5, title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', rating: 3, genre: 'Mystery', year: 1947 },
    { id: 6, title: 'Ted Lasso', price: 9.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', rating: 5, genre: 'Comedy', year: 2020 },
    // Add more dummy results as needed
  ]);
  const [sortOrder, setSortOrder] = useState('desc');
  // const [searchQuery, setSearchQuery] = useState('Movie');
  const [totalResults, setTotalResults] = useState(10);
  const [visibleGenres, setVisibleGenres] = useState(10);
  // const [loading, setLoading] = useState(false);

  const genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Fantasy', 'Adventure', 'Mystery', 'Crime', 'Animation', 'Family', 'History'];

  useEffect(() => {
    fetchMovies();
    setTotalResults(searchResults.length);
  }, [searchResults.length]);

  const fetchMovies = async () => {
    try {
      const response = await axios.get('http://localhost:8000/search');
      setSearchResults(response.data);
      console.log('Movies:', response.data);
    } catch (error) {
      console.error('Failed to fetch movies:', error);
    }
  };

  const handleGenreChange = (genre) => {
    const updatedGenres = filters.genre.includes(genre)
      ? filters.genre.filter((g) => g !== genre)
      : [...filters.genre, genre];
    setFilters({ ...filters, genre: updatedGenres });

    // Trigger search request here
    handleFilterChange();
  };

  const handlePriceChange = (e) => {
    setFilters({ ...filters, price: { ...filters.price, [e.target.name]: e.target.value } });
    // Trigger search request here if both min and max are set
    if (filters.price.min && filters.price.max) {
      handleFilterChange();
    }
  };

  const handleRatingChange = (rating) => {
    const updatedRatings = filters.rating.includes(rating)
      ? filters.rating.filter((r) => r !== rating)
      : [...filters.rating, rating];
    setFilters({ ...filters, rating: updatedRatings });

    // Trigger search request here
    handleFilterChange();
  };

  const handleFilterChange = async () => {
    // setLoading(true);
    // setTimeout(() => {
    //   setLoading(false);
    // }, 2000);
    const queryString = convertFiltersToQueryString(filters);
    try {
      const response = await axios.post(`http://localhost:8000/search?${queryString}`);
      setSearchResults(response.data);
      console.log('Genre updated successfully');
    } catch (error) {
      console.error('Failed to update genre:', error);
    } finally {
      // setLoading(false);
    }
  };

  const convertFiltersToQueryString = (filters) => {
    const { q, genre, price, rating } = filters;
    const qQuery = q ? `query=${q}` : '';
    const genreQuery = genre.length > 0 ? `genre=${genre.join(',')}` : '';
    const priceQuery = price.min && price.max ? `price=${price.min}-${price.max}` : '';
    const ratingQuery = rating.length > 0 ? `rating=${rating.join(',')}` : '';
    return [qQuery, genreQuery, priceQuery, ratingQuery].filter((q) => q).join('&');
  };

  const handleSortChange = (e) => {
    setSortOrder(e.target.value);
    // Trigger search request here
  };
  
  const handleShowMoreGenres = () => {
    setVisibleGenres(visibleGenres + 10);
  };

  // const handleSearch = async () => {
  //   const results = await fetchSearchResults(filters);
  //   setSearchResults(results);
  // };



  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar for filtering */}
      <div className="search-movie-sidebar">
        {/* Genre Filter */}
        <h4>Genres</h4>
        {genres.slice(0, visibleGenres).map((genre, index) => (
          <div key={index} className="search-movie-sidebar__item">
            <input
              type="checkbox"
              id={`genre-${genre}`}
              onChange={() => handleGenreChange(genre)}
            />
            <label htmlFor={`genre-${genre}`}>{genre}</label>
          </div>
        ))}
        {genres.length > visibleGenres && (
          <button 
            onClick={handleShowMoreGenres}
            // className=""
          >
            More
          </button>
        )}

        {/* Price Filter */}
        <h4>Price</h4>
        <input
          type="number"
          name="min"
          placeholder="Min"
          value={filters.price.min}
          onChange={handlePriceChange}
        />
        <input
          type="number"
          name="max"
          placeholder="Max"
          value={filters.price.max}
          onChange={handlePriceChange}
        />
        <button onClick={() => {/* Trigger search request here */}}>Apply</button>

        {/* Rating Filter */}
        <h4>Rating</h4>
        {[0, 1, 2, 3, 4].map((star, index) => (
          <div key={index} className="search-movie-sidebar__item">
            <input
              type="checkbox"
              id={`rating-${star}`}
              onChange={() => handleRatingChange(star)}
            />
            <label htmlFor={`rating-${star}`}>{`> ${star} stars`}</label>
          </div>
        ))}
      </div>

      {/* Search Results Area */}
      <div style={{ flex: 1, padding: '10px' }} className="search-movie__result-area">
        {/* Search Query and Sort */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
          <div>
            <h2>{searchQuery}</h2>
          </div>
          <div>
            <span>{totalResults} items found </span>
            <select value={sortOrder} onChange={handleSortChange}>
              <option value="desc">Giảm dần</option>
              <option value="asc">Tăng dần</option>
            </select>
          </div>
        </div>

        {/* Search Results List */}
        <div>
          {searchResults.map((result, index) => (
            <div key={index} style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>
              <MovieItem 
                item={result}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SearchPage;