// client/src/services/queryAgentAPI.ts
import { API_BASE_URL } from './config';

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
    if (response.status === 404) {
      throw new Error(`Error: Not Found. The API endpoint at ${fullUrl} could not be reached. Please check the backend router configuration.`);
    }
    const errorData = await response.json().catch(() => ({
      detail: 'The server responded with an unexpected format.',
    }));
    const detailMessage = typeof errorData.detail === 'object' && errorData.detail !== null
      ? (errorData.detail.message || JSON.stringify(errorData.detail))
      : errorData.detail;
    throw new Error(detailMessage || `Server error: ${response.statusText}`);
  }

  try {
    return await response.json();
  } catch {
    throw new Error('Received an invalid JSON response from the server.');
  }
};