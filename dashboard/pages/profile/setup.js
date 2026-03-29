import { getServerSession } from 'next-auth/next'
import { authOptions } from '../api/auth/[...nextauth]'
import { useState, useRef } from 'react'
import { useRouter } from 'next/router'
import supabase, { uploadProfilePhoto } from '../../lib/supabase'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (session.user.hasProfile) return { redirect: { destination: '/', permanent: false } }
  return { props: { session } }
}

export default function ProfileSetup({ session }) {
  const router = useRouter()
  const fileRef = useRef(null)
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    initial_capital: '',
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
    if (!form.initial_capital || parseFloat(form.initial_capital) < 0) errors.initial_capital = 'Enter a valid amount'
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
          initial_capital: parseFloat(form.initial_capital || 0),
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

  const isValid = form.first_name.trim() && form.last_name.trim() && form.initial_capital

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
                className="w-full bg-surface border border-border rounded-lg px-4 py-3 text-white min-h-[44px]"
              />
              {fieldErrors.first_name && <p className="text-loss text-xs mt-1">{fieldErrors.first_name}</p>}
            </div>

            <div>
              <label className="block text-sm text-neutral mb-1">Last Name</label>
              <input
                type="text" required value={form.last_name}
                onChange={e => setForm({ ...form, last_name: e.target.value })}
                className="w-full bg-surface border border-border rounded-lg px-4 py-3 text-white min-h-[44px]"
              />
              {fieldErrors.last_name && <p className="text-loss text-xs mt-1">{fieldErrors.last_name}</p>}
            </div>

            <div>
              <label className="block text-sm text-neutral mb-1">Email</label>
              <input
                type="email" readOnly value={session.user.email}
                className="w-full bg-surface/50 border border-border rounded-lg px-4 py-3 text-neutral min-h-[44px] cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block text-sm text-neutral mb-1">Initial investment amount ($)</label>
              <input
                type="number" step="0.01" min="0" required placeholder="0.00"
                value={form.initial_capital}
                onChange={e => setForm({ ...form, initial_capital: e.target.value })}
                className="w-full bg-surface border border-border rounded-lg px-4 py-3 text-white min-h-[44px]"
              />
              <p className="text-xs text-neutral mt-1">This records your starting capital contribution to the fund.</p>
              {fieldErrors.initial_capital && <p className="text-loss text-xs mt-1">{fieldErrors.initial_capital}</p>}
            </div>
          </div>

          {error && <p className="text-loss text-sm mt-4 text-center">{error}</p>}

          <button
            type="submit" disabled={loading || !isValid}
            className="w-full mt-6 bg-profit text-white font-semibold py-3 rounded-lg min-h-[48px] disabled:opacity-40 transition hover:opacity-90"
          >
            {loading ? 'Setting up...' : 'Complete Profile and Enter Dashboard'}
          </button>
        </form>
      </div>
    </div>
  )
}
