import { itApi } from "@/lib/axios";
import { 
  TicketResponse, 
  CreateTicketRequest, 
  UpdateTicketStatusRequest, 
  AssignTicketRequest,
  AssetResponse,
  CreateAssetRequest,
  UpdateAssetRequest,
  AssignAssetRequest
} from "@/types/it";
import axios from "axios";
import { ApiError } from "@/types/auth";

export const itRepository = {
  async getTickets(params?: { search?: string, status?: string, priority?: string }): Promise<TicketResponse[]> {
    try {
      const response = await itApi.get<TicketResponse[]>("/tickets", { params });
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
  },

  async updateTicketStatus(id: string, data: UpdateTicketStatusRequest): Promise<TicketResponse> {
    try {
      const response = await itApi.patch<TicketResponse>(`/tickets/${id}/status`, data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to update ticket status.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async assignTicket(id: string, data: AssignTicketRequest): Promise<TicketResponse> {
    try {
      const response = await itApi.patch<TicketResponse>(`/tickets/${id}/assign`, data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to assign ticket.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  // Assets
  async getAssets(params?: { search?: string, status?: string, category?: string }): Promise<AssetResponse[]> {
    try {
      const response = await itApi.get<AssetResponse[]>("/assets", { params });
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch assets.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async createAsset(data: CreateAssetRequest): Promise<AssetResponse> {
    try {
      const response = await itApi.post<AssetResponse>("/assets", data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to create asset.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async updateAsset(id: string, data: UpdateAssetRequest): Promise<AssetResponse> {
    try {
      const response = await itApi.put<AssetResponse>(`/assets/${id}`, data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to update asset.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async assignAsset(id: string, data: AssignAssetRequest): Promise<AssetResponse> {
    try {
      const response = await itApi.post<AssetResponse>(`/assets/${id}/assign`, data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to assign asset.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async returnAsset(id: string): Promise<AssetResponse> {
    try {
      const response = await itApi.post<AssetResponse>(`/assets/${id}/return`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to return asset.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async deleteAsset(id: string): Promise<void> {
    try {
      await itApi.delete(`/assets/${id}`);
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to delete asset.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  }
};
