import { create } from 'zustand';
import { User } from '@/types/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  isInitialized: boolean;
  setUser: (user: User, token: string) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setInitialized: (isInitialized: boolean) => void;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  isInitialized: false,
  setUser: (user, token) => set({ user, token, isAuthenticated: true, error: null }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setInitialized: (isInitialized) => set({ isInitialized }),
  logout: async () => {
    try {
      const { authRepository } = await import("@/repositories/authRepository");
      await authRepository.logout();
    } catch (e) {
      console.error("Failed to logout backend", e);
    } finally {
      set({ user: null, token: null, isAuthenticated: false, error: null });
    }
  },
}));
