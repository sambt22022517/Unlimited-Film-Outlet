import MovieList from '../components/MovieList';
import '../styles/MovieDetails.css';

function MovieDetails() {
  const data = {
    tvShows: [
      { id: 1, title: 'Presumed Innocent', genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', url: '/', ordinal: 1 },
      { id: 2, title: 'Lady in the Lake', genre: 'Thriller', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', url: '/', ordinal: 2 },
      { id: 3, title: 'Ted Lasso', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', url: '/', ordinal: 3 },
      { id: 4, title: 'Time Bandits', genre: 'Adventure', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/jy3YwHfdhEz1jLBZOdePdg/369x208.jpg', url: '/', ordinal: 4 },
      { id: 5, title: 'Land of Women', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/bAYwyYOKbVDK-JLBqGLLqg/369x208.jpg', url: '/', ordinal: 5 },
      { id: 6, title: 'Presumed Innocent', genre: 'Crime', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', url: '/', ordinal: 6 },
      { id: 7, title: 'Lady in the Lake', genre: 'Thriller', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', url: '/', ordinal: 7 },
      { id: 8, title: 'Ted Lasso', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', url: '/', ordinal: 8 },
      { id: 9, title: 'Time Bandits', genre: 'Adventure', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/jy3YwHfdhEz1jLBZOdePdg/369x208.jpg', url: '/', ordinal: 9 },
      { id: 10, title: 'Land of Women', genre: 'Comedy', imageUrl: 'https://is1-ssl.mzstatic.com/image/thumb/bAYwyYOKbVDK-JLBqGLLqg/369x208.jpg', url: '/', ordinal: 10 }
    ],
  }

  return (
    <div className="loading-inner">
      <div className="product-page">
      <div>
        {/* ---------------------------------------------------- */}
        <div className="product-header__wrapper dark-content clr-primary-text-on dark product-header__wrapper--with-color-transition"
          style={{ 'background-color': 'rgb(167, 173, 168)'}}
        >
          <div className="product-header__brand-logo">

          </div>

          <div className="product-header__image--logo">

          </div>

          {/* <div>
            <div className="product-header__video-wrapper">
              <div className="background-video__wrapper">
                <video 
                  className="background-video__media"
                  preload="auto"
                  src="https://play-edge.itunes.apple.com/WebObjects/MZPlayLocal.woa/hls/subscription/playlist.m3u8?cc=US&svcId=tvs.vds.4105&a=1712530888&isExternal=true&brandId=tvs.sbd.4000&id=705466315&l=en-US&aec=UHD"
                >
                </video>
              </div>
            </div>

            <div className="product-header__video-control__container">

            </div>
          </div> */}

          <picture>
            <source
              media="(min-width:1320px)"
              srcSet="https://is1-ssl.mzstatic.com/image/thumb/zOQ4Gz7BdkLtExHLasRDdg/1679x945sr.webp 1x, https://is1-ssl.mzstatic.com/image/thumb/zOQ4Gz7BdkLtExHLasRDdg/3358x1889sr.webp 2x"
              type="image/webp"
            />

            <img
              width={1679}
              height={945}
              src="https://is1-ssl.mzstatic.com/image/thumb/zOQ4Gz7BdkLtExHLasRDdg/1679x945sr.jpg"
              alt="The Family Plan" 
              className="product-header__image-bg product-header__image-bg--hidden"
            />
          </picture>

          <div className="product-header__main__container">
            <div className="product-header__content__container">
              <div className="product-header__blur"></div>

              <div className="product-header__content__availability-text">
                <div className="video-data-services-button__availabitity video-data-services-button__availability--dark typography-callout">
                  7 days free, then $9.99/month.
                </div>
              </div>

              <div className="product-header__content__buttons">
                <ul className="video-data-services-buttons__list">
                  <li className="video-data-services-buttons__list-item">
                    <button 
                      title="Buy"
                      className="video-data-services-button typography-title-3-emphasized" 
                      type="button"
                    >
                      <span className="video-data-services-button__text">Mua 200.000đ</span>
                    </button>
                  </li>

                  <li className="video-data-services-buttons__list-item">
                    <button
                      title="Add to Cart"
                      className="video-data-services-button typography-title-3-emphasized"
                      type="button"
                    >
                      <span className="video-data-services-button__glyph video-data-services-button__glyph--add"></span>
                      <span className="video-data-services-button__text">Thêm vào Giỏ hàng</span>
                    </button>
                  </li>
                </ul>
              </div>

              <div className="product-header__content__details">
                <div className="line-clamp-wrappep">
                  <div 
                    className="line-clamp product-header__content__details__synopsis typography-title-3"
                    style={{ '--link-length': 4 }} 
                    dir="auto" 
                  >
                    Dan Morgan is many things: a devoted husband, a loving father, a celebrated car salesman. He’s also a former assassin. And when his past catches up to his present, he’s forced to take his unsuspecting family on a road trip unlike any other.
                  </div>
                </div>

                <div className="product-header__content__details__metadata secondary-text typography-subhead-emphasized">
                  <div className="product-header__content__details__metadata--info">
                    <span>
                      Comedy
                    </span>
                    <span>
                      2024
                    </span>
                    <span>
                      1 hr 30 min
                    </span>
                  </div>
                </div>
              </div>

              <div className="product-header__content__crews typography-title-3">
                <div>
                  <span className="secondary-text">
                    Starring
                  </span>
                  <span className="product-header__content__crews__list">
                    Mark Wahlberg, Michelle Monaghan, Maggie Q
                  </span>
                </div>

                <div>
                  <span className="secondary-text">
                    Director
                  </span>
                  <span className="product-header__content__crews__list">
                    Simon Cellan Jones
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>

        {/* ---------------------------------------------------- */}
        <div className="product-main">
          <MovieList title={'Related'} items={data.tvShows} />
        </div>

        <div className="devider"></div>

        {/* ---------------------------------------------------- */}
        <div className="product-footer secondary-bg-color">

        </div>
      </div>
    </div>
  );
}

export default MovieDetails;