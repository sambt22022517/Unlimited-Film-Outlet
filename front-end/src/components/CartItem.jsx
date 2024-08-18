import '../styles/CartItem.css';

function CardItem({ item, onRemove, onAdd }) {
  return (
    <div className="cart-item">
      <img 
        src={item.imageURL}
        width={240}
        height={160}
        alt="example"
        className="cart-item-image"
      />
      <div className="cart-item-details">
        <h3 className="cart-item-title">{item.title}</h3>
        <p className="cart-item-price">{item.price}đ</p>
      </div>
      <div className="cart-item-actions">
        <input 
          type="checkbox" 
          checked={item.selected}
          onChange={() => onAdd(item.id)}
        />
        <button onClick={() => onRemove(item.id)}>Remove</button>
      </div>
    </div>
  );
}

export default CardItem;