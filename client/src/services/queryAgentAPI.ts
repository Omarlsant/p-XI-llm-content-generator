// client/src/services/queryAgentAPI.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface QueryAgentPayload {
  question: string;
  language: string;
  use_search: boolean;
  company_info: string;
}

export interface QueryAgentResponse {
  answer: string;
}

export const invokeQueryAgent = async (payload: QueryAgentPayload): Promise<QueryAgentResponse> => {
  const fullUrl = `${API_BASE_URL}/api/v1/query-agent/invoke`;
  console.log("Invoking Query Agent with payload:", payload);

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