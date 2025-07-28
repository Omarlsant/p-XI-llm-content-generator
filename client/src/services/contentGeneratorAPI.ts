// client/src/services/contentGeneratorAPI.ts

// Fallback added for safety, in case the .env variable is not set.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface GenerateContentPayload {
  topic: string;
  platforms: string[];
  model: string;
  language: string;
  company_info?: string;
  use_news_search?: boolean;
}

export interface GeneratedContentResponse {
  generated_content: { [key: string]: string; };
  image_url: string | null;
  image_alt: string | null;
}

export const generateContent = async (payload: GenerateContentPayload): Promise<GeneratedContentResponse> => {
  // --- THE ONLY CHANGE IS HERE ---
  // The backend route was changed from `/api/v1/generate` to `/api/v1/content-agent`
  // and the specific endpoint path is `/` at the end, which is optional in the fetch call.
  const fullUrl = `${API_BASE_URL}/api/v1/content-agent`;
  
  console.log("Sending ContentGen payload:", payload, "to URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    // Providing a more helpful error for 404
    if (response.status === 404) {
      throw new Error(`Error: Not Found. The API endpoint at ${fullUrl} could not be reached. Please check the backend router configuration.`);
    }
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  return response.json();
};

// --- RAG Functions (These are already correct, no changes needed) ---
export interface RAGQueryPayload { question: string; }
export interface RAGQueryResponse { answer: string; }

export const queryVectorRAG = async (payload: RAGQueryPayload): Promise<RAGQueryResponse> => {
  const fullUrl = `${API_BASE_URL}/api/v1/rag/query-vector`;
  console.log("Sending Vector RAG query payload:", payload, "to URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  return response.json();
};

export const queryGraphRAG = async (payload: RAGQueryPayload): Promise<RAGQueryResponse> => {
  const fullUrl = `${API_BASE_URL}/api/v1/rag/query-graph`;
  console.log("Sending Graph RAG query payload:", payload, "to URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  return response.json();
};