import '../styles/PurchaseHistoryItem.css';

const PurchaseHistoryItem = ({ item }) => {
  return (
    <div className="purchase-history-item">
      <h3 className="purchase-history-date">{item.date}</h3>
      <div className="purchase-history-details">
        {item.movies.map((movie, index) => (
          <div key={index} className="purchase-history-movie">
            <img src={movie.imageURL} alt={movie.title} className="purchase-history-movie-image" />
            <div className="purchase-history-movie-info">
              <p className="purchase-history-movie-title">{movie.title}</p>
              <p className="purchase-history-movie-price">{movie.price}đ</p>
            </div>
          </div>
        ))}
      </div>
      <div className="purchase-history-summary">
        <p>Total Price: {item.totalPrice}đ</p>
      </div>
    </div>
  );
};

export default PurchaseHistoryItem;