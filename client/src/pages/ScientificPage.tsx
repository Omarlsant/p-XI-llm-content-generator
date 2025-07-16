import { useState } from 'react';
import { queryRAG } from '../services/contentGeneratorAPI';

const ScientificPage = () => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await queryRAG({ question });
      setResult(data.answer);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto py-12 px-4">
      <h1 className="text-4xl font-bold text-center mb-2">
        Scientific <span className="bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-sky-500">RAG</span>
      </h1>
      <p className="text-center text-slate-400 mb-8">
        Ask questions about Large Language Models and RAG. The AI will answer based on indexed research papers.
      </p>

      <form onSubmit={handleSubmit} className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 shadow-xl space-y-8">
        <div>
          <label htmlFor="question" className="block text-lg font-medium mb-2">Your Question</label>
          <textarea
            id="question" value={question} onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ex: What are the main components of a RAG system?"
            className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500 transition-all"
            rows={4} required
          />
        </div>
        <button type="submit" disabled={loading} className="w-full text-lg bg-gradient-to-r from-teal-500 to-sky-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-sky-500/40 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed disabled:text-slate-400">
          {loading ? 'Thinking...' : 'Ask AI Assistant'}
        </button>
      </form>

      {error && (
        <div className="mt-8 bg-red-500/10 border border-red-500/30 text-red-300 p-4 rounded-lg">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="mt-10 bg-slate-800/50 p-8 rounded-xl border border-slate-700 animate-fade-in">
          <h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-sky-500">Assistant's Answer</h2>
          <div className="text-slate-300 whitespace-pre-wrap leading-relaxed prose prose-invert max-w-none">
            {result}
          </div>
        </div>
      )}
    </div>
  );
};

export default ScientificPage;