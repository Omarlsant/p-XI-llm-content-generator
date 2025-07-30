// src/components/Footer.tsx

// Make sure Link is imported from react-router-dom
import { Link } from 'react-router-dom';
import { GitHub as GitHubIcon, LinkedIn as LinkedInIcon, MailOutline as MailIcon } from '@mui/icons-material';

const Footer = () => {
  return (
    <footer className="bg-slate-900/50 pt-12 pb-8 mt-2">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-800 pt-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-center md:text-left">
          
          <div>
            <h3 className="text-2xl font-bold mb-3 bg-clip-text text-transparent bg-gray-50">
                Post
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500"> GenerAItor</span>
            </h3>
            <p className="text-slate-400 max-w-xs mx-auto md:mx-0">
              An AI tool to automate and supercharge digital content creation.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-cyan-400 mb-4 tracking-wider uppercase">Navigation</h4>
            <ul className="space-y-3 text-slate-300">
              {/* --- CORRECTED INTERNAL LINKS --- */}
              <li>
                <Link to="/generate" className="hover:text-violet-400 transition-colors">
                  Generator
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-violet-400 transition-colors">
                  About the Project
                </Link>
              </li>
              {/* This is an external link, so <a> is correct here */}
              <li>
                <a href="https://medium.com/@your-username" target="_blank" rel="noopener noreferrer" className="hover:text-violet-400 transition-colors">
                  Medium Article
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-cyan-400 mb-4 tracking-wider uppercase">Connect With Me</h4>
            <div className="flex justify-center md:justify-start space-x-6">
              <a href="https://github.com/your-username" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all">
                <GitHubIcon fontSize="large" />
              </a>
              <a href="https://linkedin.com/in/your-profile" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all">
                <LinkedInIcon fontSize="large" />
              </a>
              <a href="mailto:your-email@example.com" className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all">
                <MailIcon fontSize="large" />
              </a>
            </div>
          </div>
          
        </div>

        <div className="border-t border-slate-800 mt-12 pt-6 text-center text-slate-500">
          <p>Developed with ❤️ by Omar Lengua | © {new Date().getFullYear()}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;