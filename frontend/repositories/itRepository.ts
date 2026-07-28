import { itApi } from "@/lib/axios";
import { TicketResponse, CreateTicketRequest, UpdateTicketRequest } from "@/types/it";
import axios from "axios";
import { ApiError } from "@/types/auth";

export const itRepository = {
  async getTickets(): Promise<TicketResponse[]> {
    try {
      const response = await itApi.get<TicketResponse[]>("/tickets");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch tickets.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async getTicketById(id: string): Promise<TicketResponse> {
    try {
      const response = await itApi.get<TicketResponse>(`/tickets/${id}`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch ticket.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async createTicket(data: CreateTicketRequest): Promise<TicketResponse> {
    try {
      const response = await itApi.post<TicketResponse>("/tickets", data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to create ticket.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  }
};
