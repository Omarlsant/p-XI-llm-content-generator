// src/components/ContentForm.tsx

import { useState } from 'react';
import { generateContent } from '../services/contentGeneratorAPI';
import type { GeneratedContent, GenerateContentPayload } from '../services/contentGeneratorAPI';

const ContentForm = () => {
  const [topic, setTopic] = useState('');
  const [platforms, setPlatforms] = useState({ blog: false, X: false, instagram: false });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GeneratedContent | null>(null);

  const handlePlatformChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setPlatforms(prev => ({ ...prev, [name]: checked }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const selectedPlatforms = Object.keys(platforms).filter((p) => platforms[p as keyof typeof platforms]);
    if (selectedPlatforms.length === 0) {
      setError('Please select at least one platform.');
      setLoading(false);
      return;
    }
    const payload: GenerateContentPayload = { topic, platforms: selectedPlatforms };

    try {
      const data = await generateContent(payload);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto py-12 px-4">
      <h1 className="text-4xl font-bold text-center mb-2">
        Create Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Content</span>
      </h1>
      <p className="text-center text-slate-400 mb-8">Fill out the form below to get started.</p>
      
      <form onSubmit={handleSubmit} className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 shadow-xl">
        <div className="mb-6">
          <label htmlFor="topic" className="block text-lg font-medium mb-2">What do you want to write about?</label>
          <textarea
            id="topic" value={topic} onChange={(e) => setTopic(e.target.value)}
            placeholder="Ex: The impact of AI on modern society"
            className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            rows={4} required
          />
        </div>

        <div className="mb-8">
          <label className="block text-lg font-medium mb-3">Which platforms are you targeting?</label>
          <div className="flex flex-col sm:flex-row sm:space-x-6 space-y-3 sm:space-y-0">
            {Object.keys(platforms).map((platform) => (
              <label key={platform} htmlFor={platform} className="flex items-center cursor-pointer">
                <input type="checkbox" id={platform} name={platform} checked={platforms[platform as keyof typeof platforms]} onChange={handlePlatformChange} className="h-5 w-5 rounded-sm bg-slate-700 border-slate-600 text-cyan-600 focus:ring-cyan-500 focus:ring-offset-slate-800" />
                <span className="ml-3 text-lg capitalize">{platform}</span>
              </label>
            ))}
          </div>
        </div>

        <button type="submit" disabled={loading} className="w-full text-lg bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-500/40 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed disabled:text-slate-400">
          {loading ? 'Generating...' : 'Generate Content'}
        </button>
      </form>

      {error && (
        <div className="mt-8 bg-red-500/10 border border-red-500/30 text-red-300 p-4 rounded-lg">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="mt-10 bg-slate-800/50 p-8 rounded-xl border border-slate-700 animate-fade-in">
          <h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Generated Results</h2>
          {Object.entries(result).map(([platform, content]) => (
            <div key={platform} className="mb-8 last:mb-0">
              <h3 className="text-2xl font-semibold capitalize mb-3 border-b-2 border-slate-700 pb-2 text-cyan-400">{platform}</h3>
              <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">{content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ContentForm;