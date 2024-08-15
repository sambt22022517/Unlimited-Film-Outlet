import { 
  createBrowserRouter,
  RouterProvider, 
  Outlet,
} from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import './styles/App.css';
import MovieDetails from './pages/MovieDetails';
import NotFound from './pages/NotFound';
import Login from './pages/LoginPage';
import Register from './pages/RegisterPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <Header />
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
        path: 'movie/:id',
        element: <MovieDetails /> // Chi tiết phim
      },
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
    <RouterProvider router={router} />
  );
}

export default App;
