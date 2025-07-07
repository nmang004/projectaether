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
  isTokenValid: () => boolean;
}

// Helper function to check if token is expired
const isTokenExpired = (token: string): boolean => {
  try {
    const decoded = jwtDecode<User>(token);
    const currentTime = Math.floor(Date.now() / 1000);
    return decoded.exp < currentTime;
  } catch {
    return true; // If we can't decode, consider it expired
  }
};

export const useAuthStore = create<AuthState>((set, get) => ({
  token: (() => {
    try {
      if (typeof window === 'undefined') return null;
      const token = localStorage.getItem('aether_token');
      if (token && !isTokenExpired(token)) {
        return token;
      } else if (token) {
        // Token exists but is expired, remove it
        console.warn('Stored token is expired, removing from localStorage');
        localStorage.removeItem('aether_token');
      }
      return null;
    } catch {
      console.warn('localStorage not available');
      return null;
    }
  })(),
  user: (() => {
    try {
      if (typeof window === 'undefined') return null;
      const token = localStorage.getItem('aether_token');
      if (token && !isTokenExpired(token)) {
        try {
          return jwtDecode<User>(token);
        } catch {
          console.warn('Invalid token in localStorage');
          localStorage.removeItem('aether_token');
          return null;
        }
      }
      return null;
    } catch {
      console.warn('localStorage not available for user');
      return null;
    }
  })(),
  setToken: (token: string) => {
    try {
      if (isTokenExpired(token)) {
        console.error('Cannot set expired token');
        return;
      }
      const user = jwtDecode<User>(token);
      if (typeof window !== 'undefined') {
        localStorage.setItem('aether_token', token);
      }
      console.log('✅ Token set successfully');
      set({ token, user });
    } catch (error) {
      console.error('Invalid token:', error);
    }
  },
  logout: () => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('aether_token');
      }
    } catch {
      console.warn('Could not access localStorage for logout');
    }
    console.log('🔓 User logged out');
    set({ token: null, user: null });
  },
  isTokenValid: () => {
    const { token } = get();
    return token ? !isTokenExpired(token) : false;
  },
}));