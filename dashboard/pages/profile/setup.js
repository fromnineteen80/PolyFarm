import { getServerSession } from 'next-auth/next'
import { authOptions } from '../api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useRef } from 'react'
import { useRouter } from 'next/router'
import supabase, { uploadProfilePhoto } from '../../lib/supabase'
import { formatCurrency } from '../../lib/calculations'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (session.user.hasProfile) return { redirect: { destination: '/', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const [cfgRes, snapRes] = await Promise.all([
    sb.from('bot_config').select('*'),
    sb.from('daily_snapshots').select('wallet_value').order('date', { ascending: false }).limit(1),
  ])
  const cfg = {}
  cfgRes.data?.forEach(r => { cfg[r.key] = r.value })

  const isPaper = cfg.current_mode !== 'live'
  const paperWallet = parseFloat(snapRes.data?.[0]?.wallet_value || 1000)
  const paperAllocation = paperWallet / 2

  return { props: { session, isPaper, paperAllocation } }
}

export default function ProfileSetup({ session, isPaper, paperAllocation }) {
  const router = useRouter()
  const fileRef = useRef(null)
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    intended_capital: '',
  })
  const [photoFile, setPhotoFile] = useState(null)
  const [photoPreview, setPhotoPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})

  const handlePhotoChange = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (file.size > 5 * 1024 * 1024) {
      setError('Photo must be under 5MB')
      return
    }
    setPhotoFile(file)
    setPhotoPreview(URL.createObjectURL(file))
  }

  const validate = () => {
    const errors = {}
    if (!form.first_name.trim()) errors.first_name = 'Required'
    if (!form.last_name.trim()) errors.last_name = 'Required'
    if (!isPaper && (!form.intended_capital || parseFloat(form.intended_capital) < 0)) {
      errors.intended_capital = 'Enter a valid amount'
    }
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)
    setError('')

    try {
      let photoUrl = null
      if (photoFile) {
        photoUrl = await uploadProfilePhoto(photoFile, session.user.email)
      }

      const res = await fetch('/api/profile/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: form.first_name.trim(),
          last_name: form.last_name.trim(),
          display_name: `${form.first_name.trim()} ${form.last_name.trim()}`,
          profile_photo_url: photoUrl,
          initial_capital: isPaper ? paperAllocation : parseFloat(form.intended_capital || 0),
          intended_capital: parseFloat(form.intended_capital || 0),
          is_paper: isPaper,
        }),
      })

      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to create profile')

      router.push('/')
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const isValid = form.first_name.trim() && form.last_name.trim() && (isPaper || form.intended_capital)

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-[480px]">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-white">Welcome to PolyFarm</h1>
          <p className="text-sm text-neutral mt-2">Complete your investor profile to access the dashboard.</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-card border border-border rounded-xl p-8">
          <div className="flex justify-center mb-6">
            <button
              type="button"
              onClick={() => fileRef.current?.click()}
              className="w-24 h-24 rounded-full bg-surface border-2 border-border flex items-center justify-center overflow-hidden hover:border-profit transition min-h-[44px]"
            >
              {photoPreview ? (
                <img src={photoPreview} alt="Preview" className="w-full h-full object-cover" />
              ) : (
                <svg className="w-10 h-10 text-neutral" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              )}
            </button>
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={handlePhotoChange} />
          </div>
          <p className="text-center text-xs text-neutral mb-6">Tap to upload profile photo</p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-neutral mb-1">First Name</label>
              <input
                type="text" required value={form.first_name}
                onChange={e => setForm({ ...form, first_name: e.target.value })}
                className="input"
              />
              {fieldErrors.first_name && <p className="text-loss text-xs mt-1">{fieldErrors.first_name}</p>}
            </div>

            <div>
              <label className="block text-sm text-neutral mb-1">Last Name</label>
              <input
                type="text" required value={form.last_name}
                onChange={e => setForm({ ...form, last_name: e.target.value })}
                className="input"
              />
              {fieldErrors.last_name && <p className="text-loss text-xs mt-1">{fieldErrors.last_name}</p>}
            </div>

            <div>
              <label className="block text-sm text-neutral mb-1">Email</label>
              <input
                type="email" readOnly value={session.user.email}
                className="input input-readonly"
              />
            </div>

            {isPaper ? (
              <div>
                <label className="block text-sm text-neutral mb-1">Paper mode allocation</label>
                <div className="w-full bg-surface/50 border border-border rounded-lg px-4 py-3 text-white min-h-[44px]">
                  {formatCurrency(paperAllocation)}
                </div>
                <p className="text-xs text-paper mt-1">Paper mode is active. You are allocated half the paper wallet ({formatCurrency(paperAllocation)}) for simulated trading.</p>

                <label className="block text-sm text-neutral mb-1 mt-4">Intended real investment ($)</label>
                <input
                  type="number" step="0.01" min="0" placeholder="0.00"
                  value={form.intended_capital}
                  onChange={e => setForm({ ...form, intended_capital: e.target.value })}
                  className="input"
                />
                <p className="text-xs text-neutral mt-1">Enter the amount you plan to invest when the bot goes live. Units will recalculate automatically at that time.</p>
              </div>
            ) : (
              <div>
                <label className="block text-sm text-neutral mb-1">Initial investment amount ($)</label>
                <input
                  type="number" step="0.01" min="0" required placeholder="0.00"
                  value={form.intended_capital}
                  onChange={e => setForm({ ...form, intended_capital: e.target.value })}
                  className="input"
                />
                <p className="text-xs text-neutral mt-1">This records your starting capital contribution to the fund.</p>
                {fieldErrors.intended_capital && <p className="text-loss text-xs mt-1">{fieldErrors.intended_capital}</p>}
              </div>
            )}
          </div>

          {error && <p className="text-loss text-sm mt-4 text-center">{error}</p>}

          <button
            type="submit" disabled={loading || !isValid}
            className="btn btn-submit mt-6"
          >
            {loading ? 'Setting up...' : 'Complete Profile and Enter Dashboard'}
          </button>
        </form>
      </div>
    </div>
  )
}
