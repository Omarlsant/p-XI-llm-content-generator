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
  const fullUrl = `${API_BASE_URL}/api/v1/generate`;
  console.log("Sending payload:", payload);

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