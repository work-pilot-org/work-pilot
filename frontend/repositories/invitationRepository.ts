import { api } from "@/lib/axios";
import axios from "axios";
import { ApiError } from "@/types/auth";
import {
  InvitationCreateRequest,
  InvitationResponse,
  InvitationValidateResponse,
  AcceptInvitationRequest,
} from "@/types/invitation";

export const invitationRepository = {
  async createInvitation(data: InvitationCreateRequest): Promise<InvitationResponse> {
    try {
      const response = await api.post<InvitationResponse>("/invitations", data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to create invitation.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async listInvitations(): Promise<InvitationResponse[]> {
    try {
      const response = await api.get<InvitationResponse[]>("/invitations");
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to fetch invitations.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async resendInvitation(id: string): Promise<InvitationResponse> {
    try {
      const response = await api.post<InvitationResponse>(`/invitations/${id}/resend`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to resend invitation.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async revokeInvitation(id: string): Promise<InvitationResponse> {
    try {
      const response = await api.post<InvitationResponse>(`/invitations/${id}/revoke`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to revoke invitation.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async validateInvitation(token: string): Promise<InvitationValidateResponse> {
    try {
      const response = await api.get<InvitationValidateResponse>(`/invitations/validate/${token}`);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to validate invitation.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },

  async acceptInvitation(data: AcceptInvitationRequest): Promise<{ message: string }> {
    try {
      const response = await api.post<{ message: string }>("/invitations/accept", data);
      return response.data;
    } catch (err: unknown) {
      if (axios.isAxiosError(err) && err.response?.data) {
        const detail = (err.response.data as ApiError).detail;
        throw new Error(typeof detail === "string" ? detail : "Failed to accept invitation.");
      }
      throw new Error(err instanceof Error ? err.message : "An unexpected error occurred.");
    }
  },
};
