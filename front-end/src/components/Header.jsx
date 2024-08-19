import { useNavigate } from 'react-router-dom';
import '../styles/Header.css';

function Header() {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/login');
  };

  const handleSearch = () => {
    navigate('/search');
  };

  // const handleClickLogo = () => {
  //   navigate('/');
  // };

  return (
    <header className="header">
      <div className="logo">MyLogo</div>
      <div className="search-bar">
        <input 
          type="text" 
          placeholder="Search..." 
        />
        <form>
          <button 
            type="button"
            onClick={handleSearch}
          >
            Search
          </button>
        </form>
      </div>
      <button 
        type="button" 
        className="header__login-button"
        onClick={handleLogin}
      >
        Login
      </button>
    </header>
  );
}

export default Header;