import { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import '../styles/Login.css';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, error } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    const success = await login(username, password);
    if (success) {
      navigate('/');
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
        {error && <p style={{ color: 'red' }}>{error}</p>}
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