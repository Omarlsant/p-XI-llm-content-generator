import { useState } from 'react';
import { invokeQueryAgent } from '../services/queryAgentAPI';
import ReactMarkdown from 'react-markdown';

type QueryAgentPayload = {
  question: string;
  language: string;
  use_search: boolean;
  company_info: string;
};

const LANGUAGE_OPTIONS = { 'English': 'English', 'Spanish': 'Spanish', 'French': 'French', 'German': 'German' };

const ContentQueryPage = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{ content: string; type: 'user' | 'ai' }[]>([]);
  
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [useSearch, setUseSearch] = useState(false);
  const [companyInfo, setCompanyInfo] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    setLoading(true);
    const userMessage = { content: input, type: 'user' as const };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    // Create the structured payload object
    const payload: QueryAgentPayload = {
        question: input,
        language: selectedLanguage,
        use_search: useSearch,
        company_info: companyInfo
    };

    try {
      const data = await invokeQueryAgent(payload);
      const aiMessage = { content: data.answer, type: 'ai' as const };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err: any) {
      const errorMessage = { content: `Error: ${err.message || 'An unexpected error occurred.'}`, type: 'ai' as const };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-10rem)] w-full max-w-7xl mx-auto gap-8">
      <div className="w-full max-w-sm flex-shrink-0 bg-slate-800/50 p-6 rounded-xl border border-slate-700 shadow-xl space-y-6 overflow-y-auto">
        <h2 className="text-xl font-bold text-white">Configuration</h2>
        <div>
          <label htmlFor="lang-select" className="block text-lg font-medium mb-2 text-slate-200">Language</label>
          <select id="lang-select" value={selectedLanguage} onChange={e => setSelectedLanguage(e.target.value)} className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 appearance-none bg-no-repeat bg-right pr-8" style={{ backgroundImage: `url('data:image/svg+xml;utf8,<svg fill="rgb(156 163 175)" height="24" viewBox="0 0 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>')`, backgroundPosition: 'right 0.75rem center' }}>
            {Object.entries(LANGUAGE_OPTIONS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </div>
        <div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" checked={useSearch} onChange={e => setUseSearch(e.target.checked)} className="sr-only peer"/>
            <div className="w-11 h-6 bg-slate-600 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-600"></div>
            <span className="ml-3 text-lg font-medium text-slate-200">Use Web Search</span>
          </label>
        </div>
        <div>
          <label htmlFor="companyInfo" className="block text-lg font-medium mb-2 text-slate-200">Company Context</label>
          <textarea id="companyInfo" value={companyInfo} onChange={e => setCompanyInfo(e.target.value)} placeholder="(Optional) Provide info..." rows={5} className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500"/>
        </div>
      </div>
      <div className="w-full flex flex-col bg-slate-800/50 rounded-xl border border-slate-700 shadow-xl">
        <div className="flex-grow p-6 space-y-4 overflow-y-auto">
            {messages.length === 0 && !loading && (
                <div className="flex flex-col items-center justify-center h-full text-center text-slate-500">
                    <p className="text-2xl">Query Agent</p>
                    <p>Ask a question, and the agent will decide how to answer.</p>
                </div>
            )}
            {messages.map((msg, index) => (
                <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-xl p-4 rounded-lg shadow-md ${msg.type === 'user' ? 'bg-violet-600 text-white' : 'bg-slate-700 text-slate-200'}`}>
                       <div className="prose prose-invert max-w-none prose-p:my-2">
                         <ReactMarkdown>{msg.content}</ReactMarkdown>
                       </div>
                    </div>
                </div>
            ))}
             {loading && <div className="text-center text-slate-400">Agent is thinking...</div>}
        </div>
        <div className="p-4 border-t border-slate-700 bg-slate-900/50 rounded-b-xl">
          <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <textarea value={input} onChange={e => setInput(e.target.value)} placeholder="e.g., 'What is RAG?' or 'Write a tweet about AI trends'" className="w-full p-3 rounded-md bg-slate-700 border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500" rows={3}/>
            <button type="submit" disabled={loading} className="w-full text-lg bg-gradient-to-r from-violet-500 to-purple-600 text-white font-bold py-3 px-4 rounded-lg">
                {loading ? 'Processing...' : 'Submit to Query Agent'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContentQueryPage;