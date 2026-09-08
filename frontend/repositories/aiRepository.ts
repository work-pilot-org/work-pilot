import { aiApi } from "@/lib/axios";

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  success: boolean;
  data: string;
  conversation_id: string;
}

export interface MessageResponse {
  id: string;
  role: "user" | "ai";
  content: string;
  created_at: string;
}

export interface ConversationResponse {
  id: string;
  title: string;
  date: string;
  messages: MessageResponse[];
}

export const aiRepository = {
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await aiApi.post<ChatResponse>("/ai/chat", request);
    return response.data;
  },

  getConversations: async (): Promise<ConversationResponse[]> => {
    const response = await aiApi.get<ConversationResponse[]>("/ai/conversations");
    return response.data;
  },

  getConversation: async (id: string): Promise<ConversationResponse> => {
    const response = await aiApi.get<ConversationResponse>(`/ai/conversations/${id}`);
    return response.data;
  },

  deleteConversation: async (id: string): Promise<void> => {
    await aiApi.delete(`/ai/conversations/${id}`);
  },
};
