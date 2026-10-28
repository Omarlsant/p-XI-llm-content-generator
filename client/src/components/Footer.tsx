// src/components/Footer.tsx
import { Link } from 'react-router-dom';
import { GitHub as GitHubIcon, LinkedIn as LinkedInIcon, MailOutline as MailIcon } from '@mui/icons-material';

const Footer = () => {
  return (
    <footer className="bg-slate-900/50 pt-12 pb-8 mt-2">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-800 pt-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-center md:text-left">
          
          <div>
            <h3 className="text-2xl font-bold mb-3 bg-clip-text text-transparent bg-gray-50">
                Content
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500"> GenerAItor</span>
            </h3>
            <p className="text-slate-400 max-w-xs mx-auto md:mx-0">
              An AI-powered multi-agent suite to automate and elevate digital content creation and scientific inquiry.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-cyan-400 mb-4 tracking-wider uppercase">Navigation</h4>
            <ul className="space-y-3 text-slate-300">
              <li>
                <Link to="/generate" className="hover:text-violet-400 transition-colors">
                  Our Agents
                </Link>
              </li>
              <li>
                <Link to="/scientific-rag" className="hover:text-violet-400 transition-colors">
                  Scientific RAG
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-violet-400 transition-colors">
                  About the Project
                </Link>
              </li>
              <li>
                <a
                  href="https://github.com/Omarlsant/p-XI-llm-content-generator#readme"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-violet-400 transition-colors"
                >
                  Documentation
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-cyan-400 mb-4 tracking-wider uppercase">Connect With Me</h4>
            <div className="flex justify-center md:justify-start space-x-6">
              <a
                href="https://github.com/Omarlsant/p-XI-llm-content-generator"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="GitHub Repository"
                className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all p-2 rounded-lg"
              >
                <GitHubIcon fontSize="large" />
              </a>
              <a
                href="https://www.linkedin.com/in/omarlsant/"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="LinkedIn Profile"
                className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all p-2 rounded-lg"
              >
                <LinkedInIcon fontSize="large" />
              </a>
              <a
                href="mailto:98744809+Omarlsant@users.noreply.github.com"
                aria-label="Send email to Omar Lengua"
                className="text-slate-400 hover:text-cyan-400 hover:scale-110 transition-all p-2 rounded-lg"
              >
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
