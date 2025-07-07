import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/stores/authStore';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error] = useState('');
  const navigate = useNavigate();
  const { setToken } = useAuthStore();

  const handleLogin = () => {
    // Mock JWT token for testing - expires July 7, 2026
    const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzgzNDU3Nzc0fQ.mock_signature';
    console.log('🔐 Attempting login with mock token');
    setToken(mockToken);
    
    // Navigate to dashboard after successful login
    console.log('🧭 Navigating to dashboard');
    navigate('/', { replace: true });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login</CardTitle>
          <CardDescription>Enter your credentials to access Project Aether</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              data-testid="email-input"
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium">Password</label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              data-testid="password-input"
            />
          </div>
          {error && (
            <div className="text-red-600 text-sm" data-testid="login-error-message">
              {error}
            </div>
          )}
          <Button onClick={handleLogin} className="w-full" data-testid="login-button">
            Login
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}