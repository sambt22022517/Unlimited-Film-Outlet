import axios from "axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { SHA256 } from "crypto-js";
import '../styles/Login.css';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();

    const hashPassword = SHA256(password).toString();

    console.log('Username:', username);
    console.log('Hash Password:', hashPassword);
    
    try {
      const response = await axios.post('http://localhost:8000/login', {
        username,
        hashPassword,
      });

      if (response.status === 200) {
        alert("Bạn đã đăng nhập thành công!");
        navigate('/');
      } else {
        setError("Thông tin đăng nhập không chính xác!");
      }

      console.log(response.data);

    } catch (error) {
      setError(error.message);
      console.error('Error:', error);
    }
  };

  return (
    <div className="login-container">
      <h2>Đăng Nhập</h2>
      <form 
        action="/login"
        onSubmit={handleLogin}
      >
        <div className="form-group">
          <label htmlFor="username">Tên đăng nhập</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Mật khẩu</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className="button-login" type="submit">Đăng Nhập</button>
        {error && <div className="error-message">{error}</div>}
      </form>
      <div className="links">
        <a href="/forgot-password">Quên mật khẩu?</a>
        <br />
        <Link to="/register">Đăng ký</Link>
      </div>
    </div>
  );
}

export default Login;