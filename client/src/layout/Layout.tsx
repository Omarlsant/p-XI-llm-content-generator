import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import BackToTopButton from '../components/BackToTopButton';

const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <div className="container mx-auto py-8 px-4">
        <Outlet />
        </div>
      </main>
      <Footer />
      <BackToTopButton />
    </div>
  );
};

export default Layout;