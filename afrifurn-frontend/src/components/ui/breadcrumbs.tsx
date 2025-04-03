'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ChevronRight } from 'lucide-react'

export default function Breadcrumbs() {
  const pathname = usePathname()
  const pathSegments = pathname?.split('/').filter(segment => segment !== '') || []

  return (
    <nav aria-label="Breadcrumb" className="text-sm mb-4">
      <ol className="flex items-center space-x-2">
        <li>
          <Link href="/" className="text-gray-500 hover:text-primary transition-colors duration-200">
            Home
          </Link>
        </li>
        {pathSegments.map((segment, index) => {
          const href = `/${pathSegments.slice(0, index + 1).join('/')}`
          const isLast = index === pathSegments.length - 1
          const name = segment.charAt(0).toUpperCase() + segment.slice(1).replace('-', ' ')

          return (
            <React.Fragment key={href}>
              <ChevronRight className="h-4 w-4 text-gray-400" />
              <li>
                {isLast ? (
                  <span className="text-gray-400">{name}</span>
                ) : (
                  <Link href={href} className="text-gray-500 hover:text-primary transition-colors duration-200">
                    {name}
                  </Link>
                )}
              </li>
            </React.Fragment>
          )
        })}
      </ol>
    </nav>
  )
}