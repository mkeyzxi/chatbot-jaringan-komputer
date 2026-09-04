export interface SourceMetadata {
  source: string;
  page: number;
  score: number;
}

export interface ChatResponse {
  answer: string;
  retrieval: {
    k: number;
    sources: SourceMetadata[];
  };
  latency_ms: number;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: message }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      let errorMsg = `Server error: ${response.status}`;
      if (errorData && errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMsg = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          errorMsg = errorData.detail.map((e: any) => e.msg).join(', ');
        } else {
          errorMsg = JSON.stringify(errorData.detail);
        }
      }
      
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
