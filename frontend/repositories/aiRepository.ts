import { aiApi } from "@/lib/axios";

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  success: boolean;
  data: string;
}

export const aiRepository = {
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await aiApi.post<ChatResponse>("/ai/chat", request);
    return response.data;
  },
};
