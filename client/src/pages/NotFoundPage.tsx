import { Link } from 'react-router-dom';
import { SearchOff as NotFoundIcon, Home as HomeIcon } from '@mui/icons-material';

const NotFoundPage = () => {
  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16">
      <div className="max-w-lg w-full bg-slate-800/50 p-10 rounded-2xl border border-slate-700 text-center shadow-2xl animate-fade-in">
        <div className="w-20 h-20 mx-auto mb-6 bg-cyan-500/10 rounded-full flex items-center justify-center text-cyan-400">
          <NotFoundIcon className="h-12 w-12" />
        </div>
        <p className="text-sm font-semibold tracking-widest uppercase text-cyan-400">
          Error 404
        </p>
        <h1 className="text-4xl font-extrabold mt-2 mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">
          Page Not Found
        </h1>
        <p className="text-slate-300 mb-8 text-base leading-relaxed">
          The page you are looking for doesn't exist, has been moved, or is temporarily unavailable.
        </p>
        <Link
          to="/"
          className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-lg bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-semibold text-base transition-all shadow-lg hover:shadow-cyan-500/30 hover:-translate-y-0.5"
        >
          <HomeIcon />
          Return to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
