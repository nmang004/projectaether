import { Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';
import { ReactNode } from 'react';

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const { logout } = useAuthStore();

  console.log('🏗️ AppLayout rendering');

  try {
    return (
      <div className="min-h-screen bg-app-background">
        <div className="flex">
          {/* Glassmorphism Sidebar */}
          <aside className="w-80 glassmorphism min-h-screen fixed left-0 top-0 z-10">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-8 gradient-text font-inter">Project Aether</h2>
              <nav className="space-y-3">
                <Link
                  to="/"
                  className="flex items-center px-5 py-3 rounded-lg text-sm font-medium text-text-primary hover:bg-white/50 hover:scale-[1.02] transition-all duration-200 group"
                >
                  <span className="group-hover:text-text-primary">Dashboard</span>
                </Link>
                <Link
                  to="/site-audit"
                  className="flex items-center px-5 py-3 rounded-lg text-sm font-medium text-text-primary hover:bg-white/50 hover:scale-[1.02] transition-all duration-200 group"
                >
                  <span className="group-hover:text-text-primary">Site Audit</span>
                </Link>
                <Link
                  to="/keyword-clustering"
                  className="flex items-center px-5 py-3 rounded-lg text-sm font-medium text-text-primary hover:bg-white/50 hover:scale-[1.02] transition-all duration-200 group"
                >
                  <span className="group-hover:text-text-primary">Keyword Clustering</span>
                </Link>
              </nav>
              <div className="absolute bottom-6 left-6 right-6">
                <Button
                  variant="outline"
                  onClick={logout}
                  className="w-full"
                >
                  Logout
                </Button>
              </div>
            </div>
          </aside>

          {/* Main Content with margin for fixed sidebar */}
          <main className="flex-1 ml-80 p-8">
            <div className="animate-fade-in">
              {children}
            </div>
          </main>
        </div>
      </div>
    );
  } catch (error) {
    console.error('❌ Error in AppLayout:', error);
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h2>❌ Layout Error</h2>
        <p>Error in AppLayout: {(error as Error).toString()}</p>
      </div>
    );
  }
}