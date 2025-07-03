import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

function NotFoundPage() {
  return (
    <div className="container mx-auto py-16 text-center">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <h2 className="text-2xl font-semibold mb-4">Page Not Found</h2>
      <p className="text-muted-foreground mb-8">
        The page you're looking for doesn't exist.
      </p>
      <Button asChild>
        <Link to="/">Go Home</Link>
      </Button>
    </div>
  )
}

export default NotFoundPage