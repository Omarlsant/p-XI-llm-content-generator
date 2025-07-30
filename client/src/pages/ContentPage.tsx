import { Link } from 'react-router-dom';
import { Description as ContentIcon, QuestionAnswer as QueryIcon } from '@mui/icons-material';

const ContentPage = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
        <h1 className="text-4xl md:text-5xl font-extrabold text-center mb-4 text-slate-100">Choose Your AI Assistant</h1>
        <p className="text-slate-400 text-lg text-center max-w-2xl mb-12">
            Select an agent based on your needs. Use the Content Agent for detailed posts, or the Query Agent for quick, intelligent answers.
        </p>
        
        <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* --- Card 1: Content Agent --- */}
            <Link
                to="/generate/content-agent"
                className="group flex flex-col p-8 bg-slate-800/50 rounded-xl border border-slate-700 shadow-xl hover:border-cyan-500 hover:shadow-cyan-500/10 transition-all duration-300 transform hover:-translate-y-1"
                aria-label="Use the Content Agent"
            >
                <ContentIcon className="w-12 h-12 text-cyan-400 mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Content Agent</h2>
                <p className="text-slate-300 mb-6">
                    A specialist for creating detailed content for blogs and social media. Provides fine-grained control over platforms, languages, models, and web search.
                </p>
                <span className="mt-auto font-semibold text-cyan-400 group-hover:underline">
                    Launch Content Agent →
                </span>
            </Link>

            {/* --- Card 2: Query Agent (The unified agent) --- */}
            <Link
                to="/generate/query-agent"
                className="group flex flex-col p-8 bg-slate-800/50 rounded-xl border border-slate-700 shadow-xl hover:border-violet-500 hover:shadow-violet-500/10 transition-all duration-300 transform hover:-translate-y-1"
                aria-label="Use the Query Agent"
            >
                <QueryIcon className="w-12 h-12 text-violet-400 mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Query Agent</h2>
                <p className="text-slate-300 mb-6">
                    A conversational assistant powered by a supervisor AI. Simply ask your question, and it will route it to the right internal specialist for a quick answer.
                </p>
                <span className="mt-auto font-semibold text-violet-400 group-hover:underline">
                    Launch Query Agent →
                </span>
            </Link>
        </div>
    </div>
  );
};

export default ContentPage;