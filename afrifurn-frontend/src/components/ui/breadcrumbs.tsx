'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface BreadcrumbItem {
  name: string
  href: string
}

export default function Breadcrumbs() {
  const pathname = usePathname()
  const segments = pathname.split('/').filter(Boolean)

  // Handle room URLs by completely removing "room" from the breadcrumb display
  const crumbs: BreadcrumbItem[] = [
    { name: 'Home', href: '/' },
    ...segments
      .map((seg, idx): BreadcrumbItem | null => {
        // Skip the "room" segment entirely
        if (seg === 'room') {
          return null
        }
        
        // For segments after "room", adjust the href to include the room path
        if (segments[idx - 1] === 'room') {
          return {
            name: seg.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            href: '/' + segments.slice(0, idx + 1).join('/'),
          }
        }
        
        // Default formatting for other segments
        return {
          name: seg.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          href: '/' + segments.slice(0, idx + 1).join('/'),
        }
      })
      .filter((crumb): crumb is BreadcrumbItem => crumb !== null), // Remove null entries
  ]

  return (
    <nav className="p-4  bg-gray-50" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-0.5 px-0 py-0 text-xs md:text-sm leading-tight">
        {crumbs.map((crumb, idx) => (
          <li key={crumb.href} className="flex items-center">
            {idx > 0 && (
              <span className="mx-1 text-gray-300 select-none text-xs md:text-sm">&#8250;</span> // chevron
            )}
            {idx < crumbs.length - 1 ? (
              <Link
                href={crumb.href}
                className="text-gray-500  hover:text-primary-600 transition-colors px-0.5 py-0 rounded font-normal text-xs md:text-sm"
              >
                {crumb.name}
              </Link>
            ) : (
              <span className="font-semibold text-gray-900 px-0.5 py-0 cursor-default text-xs md:text-sm">
                {crumb.name}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}