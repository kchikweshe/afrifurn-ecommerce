'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Breadcrumbs() {
  const pathname = usePathname()
  const segments = pathname.split('/').filter(Boolean)

  // Optionally, map segments to display names or links
  const crumbs = [
    { name: 'Home', href: '/' },
    ...segments.map((seg, idx) => ({
      name: seg.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      href: '/' + segments.slice(0, idx + 1).join('/'),
    })),
  ]

  return (
    <nav
      className="py-2 px-2"
      aria-label="Breadcrumb"
    >
      <ol className="flex items-center space-x-1 bg-white/80 rounded-lg shadow-sm px-2 py-1 text-xs leading-tight">
        {crumbs.map((crumb, idx) => (
          <li key={crumb.href} className="flex items-center">
            {idx > 0 && (
              <svg
                className="mx-2 h-3 w-3 text-gray-400"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            )}
            {idx < crumbs.length - 1 ? (
              <Link
                href={crumb.href}
                className="hover:underline hover:text-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-200 transition-colors px-1 py-0.5 rounded text-gray-700 font-medium"
              >
                {crumb.name}
              </Link>
            ) : (
              <span className="font-semibold text-primary-700 px-1 py-0.5 rounded bg-primary-50 cursor-default">
                {crumb.name}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}