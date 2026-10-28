import { useState, useEffect } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { AutoAwesome as AIIcon, Menu as MenuIcon, Close as CloseIcon } from '@mui/icons-material';

const navLinkClasses = "text-slate-300 hover:text-cyan-400 transition-colors duration-300 text-lg";
const activeLinkClasses = "text-cyan-400 font-semibold";

const mobileNavLinkClasses = "block text-slate-300 hover:text-cyan-400 hover:bg-slate-800/60 rounded-lg px-4 py-3 text-lg font-medium transition-colors";
const mobileActiveLinkClasses = "text-cyan-400 bg-slate-800/80 font-semibold";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  // Close mobile menu on route change
  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  // Close mobile menu on Escape key
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen]);

  return (
    <nav className="bg-slate-900/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-slate-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          <Link to="/" className="flex items-center space-x-3 group" onClick={() => setIsOpen(false)}>
            <AIIcon className="text-cyan-400 h-9 w-9 group-hover:animate-spin" />
            <span className="text-2xl font-bold text-slate-100 tracking-wider">
              Content 
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500"> GenerAItor</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <NavLink to="/" className={({isActive}) => isActive ? `${navLinkClasses} ${activeLinkClasses}` : navLinkClasses}>
              Home
            </NavLink>
            <NavLink to="/scientific-rag" className={({isActive}) => isActive ? `${navLinkClasses} ${activeLinkClasses}` : navLinkClasses}>
              Scientific RAG
            </NavLink>
            <NavLink to="/about" className={({isActive}) => isActive ? `${navLinkClasses} ${activeLinkClasses}` : navLinkClasses}>
              About
            </NavLink>
            
            <Link
              to="/generate"
              className="bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-semibold py-2 px-5 rounded-lg shadow-md hover:shadow-lg hover:shadow-cyan-500/40 hover:-translate-y-1 transition-all duration-300"
            >
              Our Agents
            </Link>
          </div>

          {/* Mobile menu button (min 44x44px touch target) */}
          <div className="flex md:hidden">
            <button
              type="button"
              onClick={() => setIsOpen(prev => !prev)}
              aria-label={isOpen ? "Close navigation menu" : "Open navigation menu"}
              aria-expanded={isOpen}
              aria-controls="mobile-navigation-menu"
              className="w-11 h-11 flex items-center justify-center rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-colors"
            >
              {isOpen ? <CloseIcon className="h-7 w-7" /> : <MenuIcon className="h-7 w-7" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Navigation Drawer / Menu */}
      {isOpen && (
        <div
          id="mobile-navigation-menu"
          className="md:hidden border-t border-slate-800 bg-slate-900/95 px-4 pt-4 pb-6 space-y-3 animate-fade-in"
        >
          <NavLink
            to="/"
            onClick={() => setIsOpen(false)}
            className={({isActive}) => isActive ? `${mobileNavLinkClasses} ${mobileActiveLinkClasses}` : mobileNavLinkClasses}
          >
            Home
          </NavLink>
          <NavLink
            to="/scientific-rag"
            onClick={() => setIsOpen(false)}
            className={({isActive}) => isActive ? `${mobileNavLinkClasses} ${mobileActiveLinkClasses}` : mobileNavLinkClasses}
          >
            Scientific RAG
          </NavLink>
          <NavLink
            to="/about"
            onClick={() => setIsOpen(false)}
            className={({isActive}) => isActive ? `${mobileNavLinkClasses} ${mobileActiveLinkClasses}` : mobileNavLinkClasses}
          >
            About
          </NavLink>
          <div className="pt-2">
            <Link
              to="/generate"
              onClick={() => setIsOpen(false)}
              className="block w-full text-center bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-semibold py-3 px-5 rounded-lg shadow-md hover:shadow-lg hover:shadow-cyan-500/40 transition-all duration-300 text-lg"
            >
              Our Agents
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
