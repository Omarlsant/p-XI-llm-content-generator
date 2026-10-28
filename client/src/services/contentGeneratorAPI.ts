// client/src/services/contentGeneratorAPI.ts
import { API_BASE_URL } from './config';

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
  errors?: { [key: string]: string; };
  image_url: string | null;
  image_alt: string | null;
  success?: boolean;
}

export const generateContent = async (payload: GenerateContentPayload): Promise<GeneratedContentResponse> => {
  const fullUrl = `${API_BASE_URL}/api/v1/content-agent`;
  
  console.log("Sending ContentGen payload:", payload, "to URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error(`Error: Not Found. The API endpoint at ${fullUrl} could not be reached. Please check the backend router configuration.`);
    }
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  try {
    return await response.json();
  } catch {
    throw new Error('Received an invalid JSON response from the server.');
  }
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
    if (response.status === 404) {
      throw new Error(`Error: Not Found. The API endpoint at ${fullUrl} could not be reached. Please check the backend router configuration.`);
    }
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  try {
    return await response.json();
  } catch {
    throw new Error('Received an invalid JSON response from the server.');
  }
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
    if (response.status === 404) {
      throw new Error(`Error: Not Found. The API endpoint at ${fullUrl} could not be reached. Please check the backend router configuration.`);
    }
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  try {
    return await response.json();
  } catch {
    throw new Error('Received an invalid JSON response from the server.');
  }
};