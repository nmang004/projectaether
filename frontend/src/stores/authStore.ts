import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

interface User {
  sub: string;
  exp: number;
}

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('aether_token'),
  user: (() => {
    const token = localStorage.getItem('aether_token');
    if (token) {
      try {
        return jwtDecode<User>(token);
      } catch {
        return null;
      }
    }
    return null;
  })(),
  setToken: (token: string) => {
    try {
      const user = jwtDecode<User>(token);
      localStorage.setItem('aether_token', token);
      set({ token, user });
    } catch (error) {
      console.error('Invalid token:', error);
    }
  },
  logout: () => {
    localStorage.removeItem('aether_token');
    set({ token: null, user: null });
  },
}));