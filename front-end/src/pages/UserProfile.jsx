import { useEffect, useState } from 'react';
import '../styles/UserProfile.css';
import axios from 'axios';

const UserProfile = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    axios.get('/account')
    .then(response => {
      const { email, username } = response.data;
      setEmail(email);
      setUsername(username);
    })
    .catch(error => {
      console.error('Error fetching user data:', error);
    });
  }, []);

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Gửi thông tin cập nhật đến backend
    axios.put('/account', { email, username, password })
      .then(() => {
        alert('User data updated successfully');
      })
      .catch(error => console.error('Error updating user data:', error));
  };

  return (
    <div className="user-profile">
      <h1>User Profile</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={handleUsernameChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
        </div>
        <button type="submit">Update Profile</button>
      </form>
    </div>
  );
};

export default UserProfile;