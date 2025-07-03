import { Link, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';

export function AppLayout() {
  const { logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-slate-50 border-r border-border min-h-screen">
          <div className="p-6">
            <h2 className="text-xl font-semibold mb-6">Project Aether</h2>
            <nav className="space-y-2">
              <Link
                to="/"
                className="block px-3 py-2 rounded-md text-sm font-medium text-foreground hover:bg-slate-100 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                to="/site-audit"
                className="block px-3 py-2 rounded-md text-sm font-medium text-foreground hover:bg-slate-100 transition-colors"
              >
                Site Audit
              </Link>
              <Link
                to="/keyword-clustering"
                className="block px-3 py-2 rounded-md text-sm font-medium text-foreground hover:bg-slate-100 transition-colors"
              >
                Keyword Clustering
              </Link>
            </nav>
            <div className="mt-auto pt-6">
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

        {/* Main Content */}
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}