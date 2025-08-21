'use client'
const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Pricing() {
  const checkout = async () => {
    const r = await fetch(`${API}/stripe/create-checkout-session`, {
      method: 'POST'
    })
    const d = await r.json()
    if (d.session_url) window.location.href = d.session_url
  }
  return (
    <main className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-semibold">Tarifs</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="border rounded p-4">
          <h2 className="font-medium">Free</h2>
          <ul className="text-sm list-disc list-inside mt-2">
            <li>Recherche d’offres</li>
            <li>Top 10 mots‑clés</li>
          </ul>
        </div>
        <div className="border rounded p-4">
          <h2 className="font-medium">Pro</h2>
          <ul className="text-sm list-disc list-inside mt-2">
            <li>Top 50 mots‑clés</li>
            <li>Analyse CV illimitée</li>
            <li>Exports CSV</li>
          </ul>
          <button onClick={checkout} className="mt-3 px-3 py-2 bg-black text-white rounded">Passer en Pro</button>
        </div>
      </div>
    </main>
  )
}


