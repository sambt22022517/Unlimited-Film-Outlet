import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
// import SearchHeader from "./SearchBar";
import { AuthContext } from "../context/AuthContext";
import '../styles/NewHeader.css';

function NewHeader() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const { isAuthenticated, logout, setSearchQuery } = useContext(AuthContext);

  const navigate = useNavigate();

  const handleDropdown = () => {
    setIsDropdownOpen(prevState => !prevState);
  };

  const handleLogin = () => {
    navigate('/login');
  };

  const handleSearch = () => {
    navigate('/search');
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSubmitSearch = (e) => {
    e.preventDefault();
    setSearchQuery(e.target.query.value);
  };

  return (
    <div className="nav-header menu-closing">
      <div className="nav-header__wrapper">
        <div className="nav-header__content">
          {/* Only available for mobile devices */}
          <div className="nav-header__dropdown-menu"></div>

          {/* Link to AppleTV */}
          <div className="nav-header__buttons-wrapper nav-header__desktop"></div>

          {/* Logo */}
          <div className="nav-header__desktop-links nav-header__desktop">
            <a href="/" className="nav-header__link--active nav-header__link">
              <span className="tab-title">Unlimited Film OutLet</span>
            </a>
          </div>

          {/* SearchBar and User Icon */}
          <div className="nav-header__user-controls">
            {/* SearchBar */}
            {/* <SearchHeader /> */}
            <div className="search-header__search nav-header__desktop">
              <div className="search-header__search search-header__search-page">
                <label 
                  id="search-header-form-input-label"
                  className="search-header__form-input-label"
                >
                  Search
                </label>

                <form role="search" onSubmit={handleSubmitSearch}>
                  <div className="search-header__search-input-wrapper">
                    <svg height="24" viewBox="0 0 64 64" width="24" xmlns="http://www.w3.org/2000/svg" className="search-header__search-icon">
                      <path d="m26.72 50.414c5.205 0 10.005-1.683 13.932-4.488l14.773 14.773c.686.686 1.59 1.028 2.556 1.028 2.026 0 3.46-1.558 3.46-3.553 0-.935-.312-1.807-.998-2.493l-14.68-14.71c3.086-4.052 4.925-9.07 4.925-14.524 0-13.184-10.784-23.968-23.967-23.968-13.153 0-23.968 10.753-23.968 23.968 0 13.183 10.784 23.967 23.968 23.967zm0-5.174c-10.285 0-18.793-8.508-18.793-18.793 0-10.286 8.508-18.794 18.794-18.794 10.285 0 18.793 8.508 18.793 18.794 0 10.285-8.508 18.793-18.793 18.793z"></path>
                    </svg>
                    <input 
                      name="query"
                      placeholder="Search"
                      autoComplete="off"
                      className="search-header__search-input"
                      id="search-header-form-input-box"
                      type="search"
                      onClick={handleSearch}
                    />
                  </div>
                  <button
                    aria-label="Clear text"
                    className="search-header__button search-header__button--close"
                    type="reset" 
                    onClick={() => setSearchQuery('')}
                  >
                    <svg width="14" height="14" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" className="search-header__close-icon">
                      <path d="M7 14c3.83 0 7-3.177 7-7 0-3.83-3.177-7-7.007-7C3.171 0 0 3.17 0 7c0 3.823 3.177 7 7 7ZM4.694 9.882a.562.562 0 0 1-.563-.57c0-.15.055-.294.165-.397l1.901-1.908-1.9-1.901a.55.55 0 0 1-.166-.398c0-.323.247-.563.563-.563.158 0 .281.055.391.158L7 6.21l1.928-1.915a.52.52 0 0 1 .392-.165c.315 0 .57.247.57.563a.53.53 0 0 1-.172.405L7.81 7.007l1.9 1.9a.524.524 0 0 1 .172.406.57.57 0 0 1-.576.57.543.543 0 0 1-.405-.165L7 7.81 5.106 9.718a.57.57 0 0 1-.412.164Z"></path>
                    </svg>
                  </button>
                </form>

                {/* Results of searching */}
                <ul 
                  className="search-hints is-hidden"
                  role="listbox"
                  id="search-hints"
                >
                </ul>
              </div>
            </div>
            {isAuthenticated ? (
              <div className="nav-header-auth">
                <div className="ember-basic-dropdown">
                  {/* User Icon */}
                  <div 
                    className="nav-header__user-image__wrapper" 
                    role="button"
                    tabIndex={0}
                    onClick={handleDropdown}
                    aria-haspopup="true"
                    aria-expanded={isDropdownOpen}
                  >
                    <img
                      src='/avatar.jpeg'
                      width={36}
                      height={36}
                      className="nav-header__user-image"
                      alt="User Avatar"
                    />

                  </div>

                  {/* Dropdown bar */}
                  { isDropdownOpen && (
                    <div className="ember-basic-dropdown-content-wormhole-origin">
                      {/* <div className="ember-basic-dropdown-overlay"></div> */}
                      <div 
                        className="ember-view ember-basic-dropdown-content 
                          ember-basic-dropdown-content--left 
                          ember-basic-dropdown-content--below 
                          ember-basic-dropdown--transitioned-in 
                          ember-basic-dropdown-content--in-place 
                          nav-header__user-dropdown-menu__options--pointer"
                        style={{ left: '-78.5px'}}
                      >
                        <ul className="nav-header__user-dropdown-menu__options" role="menu">
                          <li className="nav-header__user-dropdown-menu__option">
                            <span className="nav-header__user-dropdown-menu__option-text">
                              <a 
                                tabIndex={0} 
                                href="account" 
                                className="ember-view nav-header__user-dropdown-menu__clickable text-truncate"
                                role="menuitem"
                              >
                                Account
                              </a>
                            </span>
                          </li>
                          <li className="nav-header__user-dropdown-menu__option">
                            <span className="nav-header__user-dropdown-menu__option-text">
                              <a 
                                tabIndex={1} 
                                href="cart" 
                                className="ember-view nav-header__user-dropdown-menu__clickable text-truncate"
                                role="menuitem"
                              >
                                Cart
                              </a>
                            </span>
                          </li>
                          <li className="nav-header__user-dropdown-menu__option">
                            <span className="nav-header__user-dropdown-menu__option-text">
                              <a 
                                tabIndex={2} 
                                href="/purchase-history" 
                                className="ember-view nav-header__user-dropdown-menu__clickable text-truncate"
                                role="menuitem"
                              >
                                Purchase History
                              </a>
                            </span>
                          </li>
                          <li className="nav-header__user-dropdown-menu__option">
                            <span className="nav-header__user-dropdown-menu__option-text">
                              <button 
                                className="nav-header__user-dropdown-menu__clickable text-truncate option--sign-out"
                                role="menuitem"
                                type="button"
                                onClick={handleLogout}
                              >
                                Sign Out
                              </button>
                            </span>
                          </li>
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <button 
                type="button" 
                className="header__login-button"
                onClick={handleLogin}
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default NewHeader;