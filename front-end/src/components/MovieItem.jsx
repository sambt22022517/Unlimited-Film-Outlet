import '../styles/MovieItem.css';

function MovieItem({ item }) {
  const url_movie = `/film/${item.id}`;
  return (
    <a 
      href={url_movie}
    >
      <div className="movie-item">
        <img 
          src={item.imageURL}
          width={240}
          height={160}
          alt="example"
          className="movie-item-image"
        />
        <div className="movie-item-details">
          <h3 className="movie-item-title">{item.title}</h3>
          <p className="movie-item-genre">{item.genre}</p>
          {/* <p className="movie-item-year">{item.year}</p> */}
          <p className="movie-item-rating">{item.rating} stars</p>
          <p className="movie-item-price">{item.price}đ</p>
        </div>
        {/* <div className="movie-item-actions">
          <input 
            type="checkbox" 
            checked={item.selected}
            onChange={() => onAdd(item.id)}
          />
          <button onClick={() => onRemove(item.id)}>Remove</button>
        </div> */}
      </div>
    </a>
  );
}

export default MovieItem;