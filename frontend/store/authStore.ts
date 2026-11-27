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
    console.log("[AUTH] Logout started");
    try {
      const { authRepository } = await import("@/repositories/authRepository");
      await authRepository.logout();
      console.log("[AUTH] Cookie cleared (backend)");
    } catch (e) {
      console.error("[AUTH] Failed to call backend logout", e);
    } finally {
      set({ user: null, token: null, isAuthenticated: false, error: null });
      console.log("[AUTH] Store cleared");

      if (typeof window !== "undefined") {
        // Clear any client-side tokens stored outside Zustand
        localStorage.clear();

        // Notify other tabs so they also clear state and redirect to login
        const channel = new BroadcastChannel("auth_channel");
        channel.postMessage("logout");
        channel.close();
        console.log("[AUTH] Logout broadcast sent");

        // Redirect to login. AuthProvider on /login skips refresh automatically
        // (NO_REFRESH_PATHS), so there will be no automatic re-authentication.
        window.location.href = window.location.origin.includes("localhost")
          ? `http://localhost:${window.location.port || 3000}/login`
          : `https://workpilot.com/login`;
      }
    }
  },
}));
