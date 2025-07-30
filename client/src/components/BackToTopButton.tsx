// src/components/BackToTopButton.tsx

import { useState, useEffect } from 'react';
import { ArrowUpward } from '@mui/icons-material';

const BackToTopButton = () => {
  // State to track whether the button should be visible
  const [isVisible, setIsVisible] = useState(false);

  // This function toggles visibility based on scroll position
  const toggleVisibility = () => {
    // Show button if page is scrolled more than 300px
    if (window.scrollY > 300) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  };

  // This function scrolls the page to the top smoothly
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth', // This is what makes the scroll smooth!
    });
  };

  // useEffect to add and remove the scroll event listener
  useEffect(() => {
    window.addEventListener('scroll', toggleVisibility);

    // Cleanup function to remove the listener when the component unmounts
    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, []);

  return (
    <>
      {isVisible && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 z-50 p-3 rounded-full bg-gradient-to-r from-cyan-200 to-violet-200 text-black shadow-lg hover:shadow-xl hover:shadow-cyan-500/40 hover:-translate-y-1 transition-all duration-300 animate-fade-in"
          aria-label="Go to top"
        >
          <ArrowUpward />
        </button>
      )}
    </>
  );
};

export default BackToTopButton;