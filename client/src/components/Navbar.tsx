// src/components/Navbar.tsx

import { Link } from 'react-router-dom';
import { AutoAwesome as AIIcon } from '@mui/icons-material';

const Navbar = () => {
  return (
    <nav className="bg-slate-900/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-slate-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          <Link to="/" className="flex items-center space-x-3 group">
            <AIIcon className="text-cyan-400 h-9 w-9 group-hover:animate-spin" />
            <span className="text-2xl font-bold text-slate-100 tracking-wider">
              Post 
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500"> GenerAItor</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-slate-300 hover:text-cyan-400 transition-colors duration-300 text-lg">
              Home
            </Link>
            <Link to="/about" className="text-slate-300 hover:text-cyan-400 transition-colors duration-300 text-lg">
              About
            </Link>
            
            <Link
              to="/generate"
              className="bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-semibold py-2 px-5 rounded-lg shadow-md hover:shadow-lg hover:shadow-cyan-500/40 hover:-translate-y-1 transition-all duration-300"
            >
              Create Content
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;