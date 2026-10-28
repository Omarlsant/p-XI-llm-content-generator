const PageLoader = () => (
  <div className="flex items-center justify-center min-h-[50vh]" role="status" aria-label="Loading page content">
    <div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" />
    <span className="sr-only">Loading page content...</span>
  </div>
);

export default PageLoader;
