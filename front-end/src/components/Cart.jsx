import { useState } from "react";
import CardItem from "./CartItem";
import "../styles/Cart.css";

function Cart({ items, onUpdate, onCheckout, onBack }) {
  const [cartItems, setCartItems] = useState(items);

  const handleRemove = (id) => {
    setCartItems(cartItems.filter((item) => item.id !== id));
    onUpdate(cartItems.filter(item => item.id !== id));
  };

  const handleAdd = (id) => {
    setCartItems(cartItems.map((item) =>
      id === item.id ? { ...item, selected: !item.selected } : item
    ));
  };

  const totalPrice = cartItems
    .filter((item) => item.selected)
    .reduce((total, item) => total + item.price, 0);

  const totalItems = cartItems.filter((item) => item.selected).length;

  return (
    <div className="cart">
      <h1>Shopping Cart</h1>
      <div className="cart-items">
        {cartItems.map(item => (
          <CardItem 
            key={item.id}
            item={item}
            onRemove={handleRemove}
            onAdd={handleAdd}
          />
        ))}
      </div>
      <div className="cart-summary">
        <p>Total Items: {totalItems}</p>
        <p>Total Price: {totalPrice}đ</p>
        <button onClick={onCheckout}>Pay</button>
        <button onClick={onBack}>Cancel</button>
      </div>
    </div>
  );
}

export default Cart;