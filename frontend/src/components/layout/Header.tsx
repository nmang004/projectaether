import { Link } from 'react-router-dom'

function Header() {
  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-xl font-bold">
            Project Aether
          </Link>
          <nav className="flex items-center space-x-4">
            <span className="text-sm text-muted-foreground">
              SEO Intelligence Platform
            </span>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header