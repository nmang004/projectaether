import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Toaster } from './components/ui/toaster';
import { AppLayout } from './components/layout/AppLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import DashboardPage from './pages/DashboardPage';
import SiteAuditPage from './pages/SiteAuditPage';
import KeywordClusteringPage from './pages/KeywordClusteringPage';
import LoginPage from './pages/LoginPage';

const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <ProtectedRoute />,
    children: [
      {
        path: '',
        element: <AppLayout />,
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: 'site-audit',
            element: <SiteAuditPage />,
          },
          {
            path: 'keyword-clustering',
            element: <KeywordClusteringPage />,
          },
        ],
      },
    ],
  },
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
      <Toaster />
    </>
  );
}

export default App