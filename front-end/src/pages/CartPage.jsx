import { useState, useEffect } from "react";
import axios from "axios";
import Cart from "../components/Cart";

function CartPage() {
  // TODO: Implement the logic to manage the cart
  // - Define the initial state of the cart
  // - Implement the logic to update the cart
  // - Implement the logic to checkout
  // - Implement the logic to go back to the home page

  // Define the initial state of the cart
  const [cart, setCart] = useState([
    { id: 1, title: 'Presumed Innocent', price: 14.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/p-dFQhrrenz0eg8_smgu9w/369x208.jpg', selected: false },
    { id: 2, title: 'Lady in the Lake', price: 19.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/SCG2BRdS-gXePqsduWlMmQ/369x208.jpg', selected: false },
    { id: 3, title: 'Ted Lasso', price: 9.99, imageURL: 'https://is1-ssl.mzstatic.com/image/thumb/ageP1PYyLi7UlNiWMva32Q/369x208.jpg', selected: false },
  ]);

  // Fetch the cart items from the server
  const fetchCartItems = () => {
    axios.get('/cart')
      .then((response) => {
        setCart(response.data);
      });
  };

  // Post the cart items to the server
  const postCartItems = (items) => {
    axios.post('/cart', items)
      .then((response) => {
        setCart(response.data);
      });
  };

  useEffect(() => {
    fetchCartItems();
  });

  useEffect(() => {
    postCartItems(cart);
  }, [cart]);
  
  // Update the cart items when the cart changes
  const handleUpdateCart = (items) => {
    setCart(items);
  };

  // Proceed to checkout
  const handleCheckout = () => {
    alert('Proceeding to checkout');
  };

  // Go back to the home page
  const handleBack = () => {
    alert('Going back to home page');
  };

  return (
    <div className="cart-page">
      <Cart 
        items={cart}
        onUpdate={handleUpdateCart}
        onCheckout={handleCheckout}
        onBack={handleBack}
      />
    </div>
  );
}

export default CartPage;