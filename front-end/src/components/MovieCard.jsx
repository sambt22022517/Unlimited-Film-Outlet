import '../styles/MovieCard.css';

function MovieCard({title, year, genre, ordinal, imageUrl }) {
  const url_movie = `/movie/${ordinal}`;
  return (
    <a 
      className="card-lockup"
      href={url_movie}
    >
      <div className="card-artwork">
        <div className="canvas-lockup">
          <div 
            className="media-artwork-v2--image-did-attempt-download media-artwork-v2__container canvas-lockup__artwork"
            style={{ paddingTop: '56.25%', height: '100%' }}>
            <picture>
              <img 
                src={imageUrl} 
                loading='lazy' 
                className="media-artwork-v2__image"
                alt={title} 

              />
            </picture>
          </div>
        </div>
      </div>

      <div className="card-content">
        <div className='card-ordinal'>
          <span className="clr-secondary-text">{ordinal}</span>
        </div>

        <div className="card-metadata">
          <div 
            // id={`title-${ordinal}`}
            className="card-title clr-primary-text lt-line-clamp lt-line-clamp--multi-line"
            style={{WebkitLineClamp: 2}}
          >
            {title}
          </div>
          <p className="card-genre clr-secondary-text">
            <span>{year}</span> · <span>{genre}</span>
          </p>
        </div>
      </div>
    </a>
  );
}

export default MovieCard;