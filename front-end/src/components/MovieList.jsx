import MovieCard from "./MovieCard";
// import '../styles/index.css';
import '../styles/MovieList.css';

function MovieList({ title, items }) {
  return (
    <div 
      className="shelf-grid shelf-grid--onhover" 
      style={{ '--shelf-arrow-offset': '12px' }}
      data-grid="C"
    >
      <div className="shelf-grid-header">
        <div className="shelf-header--with-see-all">
          <a 
            href="/" 
            // aria-label="See all top chart: Movies"
            className="typ-headline-emph"
          >
            <h2 className="typ-headline-emph">
              {title}
              {/* Save svg */}
              <svg viewBox="0 0 10 16" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"><path d="m2.6 15.6c-.3.3-.6.4-1 .4-.9 0-1.6-.7-1.6-1.5 0-.4.2-.8.5-1.1l5.9-5.4-5.9-5.4c-.3-.3-.5-.7-.5-1.1 0-.9.7-1.5 1.6-1.5.4 0 .7.1 1 .4l6.8 6.4c.4.4.6.7.6 1.2s-.2.8-.6 1.2z" opacity=".95"></path></svg>
            </h2>
          </a>
        </div>
      </div>
      <div className="shelf-grid__body">
        <ul 
          className="shelf-grid__list"
          style={{
            '--grid-rows': 1,
            '--grid-column-gap': '20px',
          }}
        >
          {items.map(item => (
            <li 
              key={item.id} 
              aria-hidden={false}
              className="shelf-grid__list-item" 
            >
              <MovieCard
                key={item.id}
                id={item.id}
                title={item.title}
                year={item.year}
                genre={item.genre}
                ordinal={item.ordinal}
                imageUrl={item.imageUrl}
              />
            </li>
          ))}
        </ul>
      </div>
      <div className="shelf-grid-nav">
        <ul>
          <li>
            <button 
              className="shelf-grid-nav__arrow shelf-grid-nav__arrow--next" 
              aria-label="Next Page"
              type="button"
            ></button>
          </li>
          <li>
            <button 
              className="shelf-grid-nav__arrow shelf-grid-nav__arrow--prev" 
              aria-label="Previous Page"
              type="button"
            ></button>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default MovieList;