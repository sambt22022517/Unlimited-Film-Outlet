import { 
  createBrowserRouter,
  RouterProvider, 
  Outlet,
} from 'react-router-dom';
// import Header from './components/Header';
import NewHeader from './components/NewHeader';
import Footer from './components/Footer';
import Home from './pages/Home';
import './styles/App.css';
import NotFound from './pages/NotFound';
import MovieDetails from './pages/MovieDetails';
import Login from './pages/LoginPage';
import Register from './pages/RegisterPage';
import UserProfile from './pages/UserProfile';
import CartPage from './pages/CartPage';
import PurchaseHistoryPage from './pages/PurchaseHistoryPage';
import SearchPage from './pages/SearchPage';
import AuthProvider from './context/AuthContext';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <NewHeader />
        <main>
          <Outlet /> {/* Chỗ để các thành phần con render */}
        </main>
        <Footer />
      </>
    ),
    errorElement: <NotFound />, // Trang lỗi toàn cục
    children: [
      {
        index: true,
        element: <Home /> // Trang chính
      },
      {
        path: 'film/:id',
        element: <MovieDetails /> // Chi tiết phim
      },
      {
        path: 'account',
        element: <UserProfile /> // Trang tài khoản
      },
      {
        path: 'cart',
        element: <CartPage /> // Trang giỏ hàng
      },
      {
        path: 'purchase-history',
        element: <PurchaseHistoryPage /> // Trang lịch sử mua hàng
      },
      {
        path: 'search',
        element: <SearchPage /> // Trang tìm kiếm
      }
    ]
  },
  {
    path: 'login',
    element: <Login />, // Trang đăng nhập
  },
  {
    path: 'register',
    element: <Register />, // Trang đăng ký
  },
]);

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
