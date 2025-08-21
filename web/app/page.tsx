'use client'
import { useEffect, useMemo, useState } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type Job = {
  id: number
  title: string
  company?: string
  location?: string
  sector?: string
  contract_type?: string
  posted_at?: string | null
  url: string
}

type Keyword = { term: string; ngram: number; freq: number; tfidf: number }

export default function Home() {
  const [q, setQ] = useState('')
  const [jobs, setJobs] = useState<Job[]>([])
  const [total, setTotal] = useState(0)
  const [keywords, setKeywords] = useState<Keyword[]>([])
  const [resumeText, setResumeText] = useState('')
  const [missing, setMissing] = useState<string[]>([])
  const [coverage, setCoverage] = useState(0)
  const [plan, setPlan] = useState<'free'|'pro'>('free')

  useEffect(() => {
    fetch(`${API}/me`, { credentials: 'include' })
      .then(r => r.ok ? r.json() : { plan: 'free' })
      .then(d => setPlan((d.plan === 'pro') ? 'pro' : 'free'))
      .catch(() => setPlan('free'))
    fetch(`${API}/jobs?page=1&page_size=20&q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(d => { setJobs(d.items || []); setTotal(d.total || 0) })
      .catch(() => {})
  }, [q])

  useEffect(() => {
    fetch(`${API}/keywords?topk=20&q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(d => setKeywords(d || []))
      .catch(() => {})
  }, [q])

  // Gating simple: Free=10, Pro=50 (mock: interroge /me, ici on suppose Free)
  const limit = plan === 'pro' ? 50 : 10
  const essentialTerms = useMemo(() => keywords.slice(0, limit).map(k => k.term), [keywords])

  const analyze = async () => {
    const r = await fetch(`${API}/resume/analyze`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ resume_text: resumeText, terms: essentialTerms })
    })
    const d = await r.json()
    setMissing(d.missing_terms || [])
    setCoverage(d.coverage || 0)
  }

  return (
    <main className="grid md:grid-cols-3 gap-6">
      <section className="md:col-span-2 space-y-4">
        <div className="flex gap-2">
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Recherche..." className="flex-1 border px-3 py-2 rounded" />
          <span className="text-sm text-gray-500 self-center">Total: {total}</span>
        </div>
        <div className="space-y-2">
          {jobs.map(j => (
            <a key={j.id} href={j.url} target="_blank" className="block border rounded p-3 hover:bg-gray-50">
              <div className="font-medium">{j.title}</div>
              <div className="text-sm text-gray-600">{j.company || '—'} · {j.location || '—'} · {j.contract_type || '—'}</div>
            </a>
          ))}
        </div>
      </section>
      <aside className="space-y-6">
        <div>
          <h2 className="font-semibold mb-2">Top mots‑clés</h2>
          <ul className="space-y-1">
            {keywords.map(k => (
              <li key={k.term} className="flex justify-between text-sm">
                <span>{k.term}</span>
                <span className="text-gray-500">{k.freq || 0}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h2 className="font-semibold mb-2">Assistant CV</h2>
          <textarea value={resumeText} onChange={e=>setResumeText(e.target.value)} className="w-full border rounded p-2 h-40" placeholder="Collez ici votre CV en texte..." />
          <button onClick={analyze} className="mt-2 px-3 py-2 bg-black text-white rounded">Analyser</button>
          <div className="mt-2 text-sm">Couverture: {coverage}%</div>
          <ul className="mt-2 list-disc list-inside text-sm">
            {missing.map(m => <li key={m}>{m}</li>)}
          </ul>
        </div>
      </aside>
    </main>
  )
}


