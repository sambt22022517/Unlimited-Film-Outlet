import { createContext, useState } from 'react';
import { SHA256 } from 'crypto-js';
import axios from 'axios';

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  // const [user, setUser] = useState(null);

  // const [loading, setLoading] = useState(true);

  // useEffect(() => {
  //   const checkUser = async () => {
  //     try {
  //       const response = await axios.get('/api/user', {
  //         withCredentials: true, // Gửi cookie session
  //       });
  //       setUser(response.data);
  //     } catch (err) {
  //       setUser(null);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   checkUser();
  // }, []);

  const login = async (username, password) => {
    try {
      const hashPassword = SHA256(password).toString();

      await axios.post('http://localhost:8000/login', {
        "username": username,
        "password": hashPassword,
      }, {
        withCredentials: true,
      });
      setIsAuthenticated(true);
      alert("Bạn đã đăng nhập thành công!");
      return true;

    } catch (error) {
      // Kiểm tra chi tiết lỗi để xác định vấn đề
      if (error.response) {
        // Máy chủ trả về lỗi với mã trạng thái và thông tin
        const status = error.response.status;
        if (status === 401) {
          setError("Thông tin đăng nhập không chính xác!");
        } else if (status === 403) {
          setError("Bạn không có quyền truy cập!");
        } else {
          setError(`Lỗi không xác định: ${status}`);
        }
      } else if (error.request) {
        // Không nhận được phản hồi từ máy chủ
        setError("Không nhận được phản hồi từ máy chủ.");
      } else {
        // Lỗi khi cấu hình yêu cầu
        setError("Đã xảy ra lỗi khi cấu hình yêu cầu.");
      }

      console.error('Error:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await axios.post('http://localhost:8000/logout', {}, {
        withCredentials: true,
      });
      setIsAuthenticated(false);
      // navigate('/');
    } catch (error) {
      console.error('Error:', error);
      setError("Đã xảy ra lỗi trong quá trình đăng nhập.");
    }
  };



  return (
    <AuthContext.Provider value={{ login, logout, setSearchQuery, isAuthenticated, error, searchQuery }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;