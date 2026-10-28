import { useRouteError, isRouteErrorResponse, Link } from 'react-router-dom';
import { WarningAmber as WarningIcon, Home as HomeIcon } from '@mui/icons-material';

const RouteError = () => {
  const error = useRouteError();

  let errorMessage = 'An unexpected application error occurred.';
  let statusCode = 500;

  if (isRouteErrorResponse(error)) {
    statusCode = error.status;
    errorMessage = error.statusText || error.data?.message || 'Page error encountered.';
  } else if (error instanceof Error) {
    errorMessage = error.message;
  }

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16">
      <div className="max-w-md w-full bg-slate-800/60 p-8 rounded-2xl border border-red-500/30 text-center shadow-2xl animate-fade-in">
        <div className="w-16 h-16 mx-auto mb-4 bg-red-500/10 rounded-full flex items-center justify-center text-red-400">
          <WarningIcon className="h-10 w-10" />
        </div>
        <p className="text-sm font-semibold tracking-wider uppercase text-red-400">
          Error {statusCode}
        </p>
        <h1 className="text-3xl font-bold mt-2 mb-4 text-white">Something Went Wrong</h1>
        <p className="text-slate-300 mb-6 text-sm leading-relaxed">
          {errorMessage}
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="px-5 py-2.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white font-medium text-sm transition-colors"
          >
            Try Again
          </button>
          <Link
            to="/"
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-medium text-sm transition-all shadow-md"
          >
            <HomeIcon fontSize="small" />
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RouteError;
