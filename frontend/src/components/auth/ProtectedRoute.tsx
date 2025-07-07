import { Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { token, isTokenValid } = useAuthStore();

  console.log('🔒 ProtectedRoute check, token exists:', !!token);
  
  const tokenIsValid = token && isTokenValid();
  console.log('🔍 Token valid:', tokenIsValid);

  if (!tokenIsValid) {
    console.log('🔄 No valid token, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  console.log('✅ Valid token exists, rendering protected content');
  return <>{children}</>;
}