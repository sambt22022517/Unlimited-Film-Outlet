import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../styles/Register.css';
import { SHA256 } from "crypto-js";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";

function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [termsAccepted, setTermsAccepted] = useState(false);
  const navigate = useNavigate();

  const { login } = useContext(AuthContext);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Mật khẩu không khớp!");
      return;
    }
    if (!termsAccepted) {
      alert("Bạn phải đồng ý với các điều khoản!");
      return;
    }

    const hashPassword = SHA256(password).toString();

    try {
      const response = await axios.post('http://localhost:8000/register', {
        "email": email,
        "username": username,
        "password": hashPassword,
      });

      if (response.status === 200) {
        const { sessionToken } = response.data;
        login(sessionToken);
        alert("Đăng ký thành công!");
        console.log('Registering with', { email, username, password });
        navigate('/');
      } else if (response.status === 201) {
        alert("Tên đăng nhập hoặc email đã tồn tại!");
      } else {
        alert("Đăng ký thất bại!");
      }
    } catch (err) {
      console.error('Error:', err);
    }
  };

  const handleCancel = () => {
    setEmail('');
    setUsername('');
    setPassword('');
    setConfirmPassword('');
    setTermsAccepted(false);
  };

  return (
    <div className="register-container">
      <h2>Đăng Ký</h2>
      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
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
        <div className="form-group">
          <label htmlFor="confirm-password">Nhập lại mật khẩu</label>
          <input
            type="password"
            id="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="checkbox"
            id="terms"
            checked={termsAccepted}
            onChange={(e) => setTermsAccepted(e.target.checked)}
          />
          <label htmlFor="terms"> Tôi đồng ý với các điều khoản và điều kiện</label>
        </div>
        <button type="submit" className="register-submit-button">Đăng Ký</button>
        <button type="button" onClick={handleCancel} className="cancel-button">
          Huỷ
        </button>
      </form>
    </div>
  );
}

export default Register;