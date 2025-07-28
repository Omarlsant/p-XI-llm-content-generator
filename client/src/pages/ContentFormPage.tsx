import { useState } from 'react';
import { generateContent } from '../services/contentGeneratorAPI';
import type { GenerateContentPayload } from '../services/contentGeneratorAPI';
import type { GeneratedContentResponse } from '../services/contentGeneratorAPI';
import ReactMarkdown from 'react-markdown';

const MODEL_OPTIONS = {
  'llama3': 'Llama 3 (Local)',
  'gemini-1.5-flash': 'Gemini 1.5 Flash (Google)',
};

const LANGUAGE_OPTIONS = {
  'English': 'English', 'Spanish': 'Spanish', 'French': 'French',
  'German': 'German', 'Japanese': 'Japanese', 'Italian': 'Italian'
};

const ContentFormPage = () => {
  const [topic, setTopic] = useState('');
  const [platforms, setPlatforms] = useState({ blog: true, X: false, instagram: false });
  const [companyInfo, setCompanyInfo] = useState('');
  const [selectedModel, setSelectedModel] = useState<keyof typeof MODEL_OPTIONS>('llama3');
  const [selectedLanguage, setSelectedLanguage] = useState<keyof typeof LANGUAGE_OPTIONS>('English');
  const [useNewsSearch, setUseNewsSearch] = useState(false); // The state for the checkbox

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GeneratedContentResponse | null>(null);

  const handlePlatformChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPlatforms(prev => ({ ...prev, [e.target.name]: e.target.checked }));
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
    
    // --- THIS IS THE ONLY CHANGE REQUIRED ---
    // The payload must include `use_news_search` key with the `useNewsSearch` state value.
    const payload: GenerateContentPayload = {
      topic,
      platforms: selectedPlatforms,
      model: selectedModel,
      language: selectedLanguage,
      company_info: companyInfo || undefined,
      use_news_search: useNewsSearch, // The crucial line was missing.
    };
    
    try {
      const data = await generateContent(payload);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally { 
      setLoading(false); 
    }
  };

  // The entire JSX part was already correct.
  // The only fix needed was in the handleSubmit logic above.
  return (
    <div className="w-full max-w-3xl mx-auto py-12 px-4">
      <h1 className="text-4xl font-bold text-center mb-2">Create Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Content</span></h1>
      <p className="text-center text-slate-400 mb-8">Fill out the form below to get started.</p>
      
      <form onSubmit={handleSubmit} className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 shadow-xl space-y-8">
        <div>
          <label htmlFor="topic" className="block text-lg font-medium mb-2">What do you want to write about?</label>
          <textarea id="topic" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Ex: The impact of AI on modern society" className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500" rows={4} required />
        </div>
        <div>
          <label htmlFor="companyInfo" className="block text-lg font-medium mb-2">Company / Brand Information <span className="text-sm text-slate-400">(Optional)</span></label>
          <textarea id="companyInfo" value={companyInfo} onChange={(e) => setCompanyInfo(e.target.value)} placeholder="Ex: We are a startup that sells eco-friendly coffee mugs..." className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500" rows={3} />
        </div>
        <div>
          <label className="block text-lg font-medium mb-3">Which platforms are you targeting?</label>
          <div className="flex flex-col sm:flex-row sm:space-x-6 space-y-3 sm:space-y-0">
            {Object.keys(platforms).map((platform) => (
              <label key={platform} htmlFor={platform} className="flex items-center cursor-pointer">
                <input type="checkbox" id={platform} name={platform} checked={platforms[platform as keyof typeof platforms]} onChange={handlePlatformChange} className="h-5 w-5 rounded-sm bg-slate-700 border border-slate-600 text-cyan-600 focus:ring-cyan-500 focus:ring-offset-slate-800" />
                <span className="ml-3 text-lg capitalize">{platform}</span>
              </label>
            ))}
          </div>
        </div>
        <div className="space-y-4">
            <label className="block text-lg font-medium">Advanced Options</label>
            <div className="relative flex items-start">
                <div className="flex h-6 items-center">
                <input
                    id="news-search"
                    name="news-search"
                    type="checkbox"
                    checked={useNewsSearch}
                    onChange={(e) => setUseNewsSearch(e.target.checked)}
                    className="h-5 w-5 rounded-sm bg-slate-700 border-slate-600 text-cyan-600 focus:ring-cyan-500 focus:ring-offset-slate-800"
                />
                </div>
                <div className="ml-3 text-sm leading-6">
                <label htmlFor="news-search" className="font-medium text-slate-200">Enable Live News Search</label>
                <p id="news-search-description" className="text-slate-400">
                    Slower, but uses real-time news for topics about current events or finance.
                </p>
                </div>
            </div>
        </div>
        <div>
          <label htmlFor="language-select" className="block text-lg font-medium mb-2">Select Language</label>
          <select id="language-select" value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value as keyof typeof LANGUAGE_OPTIONS)} className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 appearance-none bg-no-repeat bg-right pr-8" style={{ backgroundImage: `url('data:image/svg+xml;utf8,<svg fill="rgb(156 163 175)" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>')`, backgroundPosition: 'right 0.75rem center' }}>
            {Object.entries(LANGUAGE_OPTIONS).map(([value, label]) => (<option key={value} value={value}>{label}</option>))}
          </select>
        </div>
        <div>
          <label htmlFor="model-select" className="block text-lg font-medium mb-2">Choose an AI Model</label>
          <select id="model-select" value={selectedModel} onChange={(e) => setSelectedModel(e.target.value as keyof typeof MODEL_OPTIONS)} className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 appearance-none bg-no-repeat bg-right pr-8" style={{ backgroundImage: `url('data:image/svg+xml;utf8,<svg fill="rgb(156 163 175)" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>')`, backgroundPosition: 'right 0.75rem center' }}>
            {Object.entries(MODEL_OPTIONS).map(([value, label]) => (<option key={value} value={value}>{label}</option>))}
          </select>
        </div>
        <button type="submit" disabled={loading} className="w-full text-lg bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-500/40 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed disabled:text-slate-400">
          {loading ? 'Generating...' : 'Generate Content'}
        </button>
      </form>
      
      {error && (<div className="mt-8 bg-red-500/10 border border-red-500/30 text-red-300 p-4 rounded-lg"><strong>Error:</strong> {error}</div>)}
      {result && (
        <div className="mt-10 bg-slate-800/50 p-8 rounded-xl border border-slate-700 animate-fade-in">
          <h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">Generated Results</h2>
          {result.image_url && (<div className="mb-8 rounded-lg overflow-hidden shadow-lg"><img src={result.image_url} alt={result.image_alt || ''} className="w-full h-auto object-cover" /></div>)}
          {Object.entries(result.generated_content).map(([platform, content]) => (
            <div key={platform} className="mb-8 last:mb-0">
              <h3 className="text-2xl font-semibold capitalize mb-4 border-b-2 border-slate-700 pb-2 text-cyan-400">{platform}</h3>
              <div className="prose prose-invert max-w-none prose-headings:text-slate-100 prose-a:text-violet-400">
                <ReactMarkdown>{content}</ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ContentFormPage;