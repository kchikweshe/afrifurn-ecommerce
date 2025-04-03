'use client'

export default function Footer() {
  return (
    <footer className="bg-white text-neutral-800 py-16 border-t">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div>
            <h3 className="text-sm font-bold mb-6 uppercase tracking-wider">About Us</h3>
            <ul className="space-y-4 text-sm">
              <li><a href="/about" className="hover:underline">Our Story</a></li>
              <li><a href="/design" className="hover:underline">Design Philosophy</a></li>
              <li><a href="/sustainability" className="hover:underline">Sustainability</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-bold mb-6 uppercase tracking-wider">Customer Care</h3>
            <ul className="space-y-4 text-sm">
              <li><a href="/contact" className="hover:underline">Contact Us</a></li>
              <li><a href="/shipping" className="hover:underline">Shipping</a></li>
              <li><a href="/returns" className="hover:underline">Returns</a></li>
              <li><a href="/faq" className="hover:underline">FAQ</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-bold mb-6 uppercase tracking-wider">Resources</h3>
            <ul className="space-y-4 text-sm">
              <li><a href="/catalog" className="hover:underline">Request Catalog</a></li>
              <li><a href="/trade" className="hover:underline">Trade Program</a></li>
              <li><a href="/financing" className="hover:underline">Financing</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-bold mb-6 uppercase tracking-wider">Connect</h3>
            <p className="text-sm mb-4">Sign up for exclusive updates and offers.</p>
            <input 
              type="email" 
              placeholder="Enter your email"
              className="w-full p-2 border border-neutral-300 mb-4"
            />
            <div className="flex space-x-6 mt-6">
              <a href="https://www.facebook.com/share/1LHgXS89qf/" className="text-neutral-800 hover:text-neutral-600">Facebook</a>
              <a href="https://www.instagram.com/afrifurn?igsh=MTM1eXpkdW94ajZ1eg==" className="text-neutral-800 hover:text-neutral-600">Instagram</a>
            </div>
          </div>
        </div>
        <div className="mt-16 pt-8 border-t text-xs text-neutral-500">
          <p>&copy; 2024 AfrifurnShop. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
} 