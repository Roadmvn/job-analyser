'use client'
import { useEffect, useState } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Account() {
  const [email, setEmail] = useState('')
  const [plan, setPlan] = useState('free')
  useEffect(() => {
    fetch(`${API}/me`, { credentials: 'include' })
      .then(r => r.ok ? r.json() : { email: '', plan: 'free' })
      .then(d => { setEmail(d.email || ''); setPlan(d.plan || 'free') })
      .catch(() => {})
  }, [])
  return (
    <main className="space-y-2">
      <h1 className="text-2xl font-semibold">Compte</h1>
      <div className="text-sm">Email: {email || 'non connecté'}</div>
      <div className="text-sm">Plan: {plan}</div>
    </main>
  )
}


