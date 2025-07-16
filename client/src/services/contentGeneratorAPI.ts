const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface GenerateContentPayload {
  topic: string;
  platforms: string[];
  model: string;
  company_info?: string;
}

export interface GeneratedContent {
  [key: string]: string;
}

export const generateContent = async (payload: GenerateContentPayload): Promise<GeneratedContent> => {
  // The backend router was updated to have a /generate prefix for this endpoint group
  const fullUrl = `${API_BASE_URL}/api/v1/generate/generate`; 
  console.log("Sending ContentGen payload:", payload);
  console.log("To URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
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

export interface RAGQueryPayload {
  question: string;
}

export interface RAGQueryResponse {
  answer: string;
}

export const queryRAG = async (payload: RAGQueryPayload): Promise<RAGQueryResponse> => {
  // The backend router has a /rag prefix for this endpoint group
  const fullUrl = `${API_BASE_URL}/api/v1/rag/query`;
  console.log("Sending RAG query payload:", payload);
  console.log("To URL:", fullUrl);

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
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