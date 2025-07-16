const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// 2. Defining types for better type safety and autocompletion.
export interface GenerateContentPayload {
  topic: string;
  platforms: string[];
}

export interface GeneratedContent {
  [key: string]: string;
}

// 3. The asynchronous function that makes the API call
export const generateContent = async (payload: GenerateContentPayload): Promise<GeneratedContent> => {
  // Construct the full URL
  const fullUrl = `${API_BASE_URL}/api/v1/generate`;
  console.log(`Sending request to: ${fullUrl}`); // Good for debugging

  const response = await fetch(fullUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  // If the response is not "ok" (e.g. status 400, 500), we throw an error.
  if (!response.ok) {
    const errorData = await response.json().catch(() => {
        // This catch block runs if the error response isn't valid JSON
        return { detail: 'The server responded with an unexpected format.' };
    });
    // Now, `errorData.detail` will always exist.
    throw new Error(errorData.detail || `Server error: ${response.statusText}`);
  }

  // If everything went well, we return the data as JSON.
  return response.json();
};