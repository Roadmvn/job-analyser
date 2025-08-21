import './globals.css'
import type { ReactNode } from 'react'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <div className="max-w-6xl mx-auto p-4">
          <header className="py-4 mb-6 border-b">
            <h1 className="text-2xl font-semibold">Job Analyser</h1>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}


