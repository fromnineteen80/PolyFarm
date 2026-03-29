import { getServerSession } from 'next-auth/next'
import { authOptions } from '../api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import { useState, useRef } from 'react'
import Layout from '../../components/Layout'
import StatCard from '../../components/StatCard'
import ExportButton from '../../components/ExportButton'
import { formatCurrency, calcInvestorValue, calcOwnershipPct } from '../../lib/calculations'
import { uploadProfilePhoto } from '../../lib/supabase'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }

  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const email = session.user.email

  const [profileRes, investorRes, eventsRes, cfgRes, snapRes] = await Promise.all([
    sb.from('investor_profiles').select('*').eq('email', email).single(),
    sb.from('investors').select('*').eq('email', email).single(),
    sb.from('capital_events').select('*').or(`first_name.eq.${session.user.profile?.first_name},email.eq.${email}`).order('timestamp', { ascending: false }),
    sb.from('bot_config').select('*'),
    sb.from('daily_snapshots').select('wallet_value').order('date', { ascending: false }).limit(1),
  ])

  const cfg = {}
  cfgRes.data?.forEach(r => { cfg[r.key] = r.value })

  return {
    props: {
      session,
      profile: profileRes.data || null,
      investor: investorRes.data || null,
      events: eventsRes.data || [],
      totalUnits: parseFloat(cfg.total_units_outstanding || 0),
      walletValue: parseFloat(snapRes.data?.[0]?.wallet_value || 0),
      isPaper: cfg.current_mode !== 'live',
    }
  }
}

export default function Profile({ session, profile, investor, events, totalUnits, walletValue, isPaper }) {
  const fileRef = useRef(null)
  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState({
    first_name: profile?.first_name || '',
    last_name: profile?.last_name || '',
    display_name: profile?.display_name || '',
  })
  const [saving, setSaving] = useState(false)
  const [photoUrl, setPhotoUrl] = useState(profile?.profile_photo_url)
  const [addCapitalOpen, setAddCapitalOpen] = useState(false)
  const [capitalAmount, setCapitalAmount] = useState('')
  const [capitalMsg, setCapitalMsg] = useState('')

  const units = parseFloat(investor?.units_held || 0)
  const ownershipPct = calcOwnershipPct(units, totalUnits)
  const currentValue = calcInvestorValue(units, totalUnits, walletValue)
  const totalInvested = events
    .filter(e => e.event_type !== 'withdrawal')
    .reduce((s, e) => s + parseFloat(e.amount || 0), 0)
  const totalWithdrawn = events
    .filter(e => e.event_type === 'withdrawal')
    .reduce((s, e) => s + parseFloat(e.amount || 0), 0)
  const netInvested = totalInvested - totalWithdrawn
  const totalReturn = currentValue - netInvested
  const returnPct = netInvested > 0 ? (totalReturn / netInvested) * 100 : 0

  const handlePhotoUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file || file.size > 5 * 1024 * 1024) return
    try {
      const url = await uploadProfilePhoto(file, session.user.email)
      setPhotoUrl(url)
      await fetch('/api/profile/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_photo_url: url }),
      })
    } catch (err) {
      console.error('Photo upload error:', err)
    }
  }

  const handleSaveProfile = async () => {
    setSaving(true)
    await fetch('/api/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm),
    })
    setSaving(false)
    setEditing(false)
  }

  const handleAddCapital = async () => {
    const amt = parseFloat(capitalAmount)
    if (!amt || amt <= 0) return
    setCapitalMsg('')
    const res = await fetch('/api/capital-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: profile?.first_name,
        last_name: profile?.last_name,
        email: session.user.email,
        event_type: 'additional',
        date: new Date().toISOString().split('T')[0],
        amount: amt,
        notes: 'Added via profile page',
      }),
    })
    const data = await res.json()
    if (data.success) {
      setCapitalMsg(`Added ${formatCurrency(amt)} to your account`)
      setCapitalAmount('')
    } else {
      setCapitalMsg(data.error || 'Error')
    }
  }

  const initial = (profile?.first_name || '?')[0].toUpperCase()

  return (
    <Layout>
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <button onClick={() => fileRef.current?.click()} className="w-[120px] h-[120px] rounded-full bg-surface border-2 border-border overflow-hidden hover:border-profit transition min-h-[44px]">
                {photoUrl ? (
                  <img src={photoUrl} alt="Profile" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-3xl font-bold text-neutral">{initial}</span>
                )}
              </button>
              <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={handlePhotoUpload} />
            </div>

            {editing ? (
              <div className="space-y-3 text-left">
                <input value={editForm.first_name} onChange={e => setEditForm({ ...editForm, first_name: e.target.value })}
                  className="input" placeholder="First Name" />
                <input value={editForm.last_name} onChange={e => setEditForm({ ...editForm, last_name: e.target.value })}
                  className="input" placeholder="Last Name" />
                <input value={editForm.display_name} onChange={e => setEditForm({ ...editForm, display_name: e.target.value })}
                  className="input" placeholder="Display Name" />
                <div className="flex gap-2">
                  <button onClick={handleSaveProfile} disabled={saving} className="btn btn-success flex-1">{saving ? 'Saving...' : 'Save'}</button>
                  <button onClick={() => setEditing(false)} className="btn btn-outline flex-1">Cancel</button>
                </div>
              </div>
            ) : (
              <>
                <h2 className="text-xl font-bold">{profile?.display_name || `${profile?.first_name} ${profile?.last_name}`}</h2>
                <p className="text-sm text-neutral">{session.user.email}</p>
                <p className="text-xs text-neutral mt-1">Member since {profile?.joined_date}</p>
                <button onClick={() => setEditing(true)} className="btn btn-ghost mt-3 text-sm">Edit Profile</button>
              </>
            )}
          </div>
        </div>

        <div className="lg:col-span-2">
          {isPaper && (
            <div className="card mb-4 border-paper border text-sm">
              <p className="text-paper font-semibold mb-1">Paper Mode Active</p>
              <p className="text-neutral">Your current allocation is simulated at {formatCurrency(netInvested)} (half the paper wallet).</p>
              {profile?.intended_capital > 0 && (
                <p className="text-neutral mt-1">Intended real investment: <span className="text-white font-semibold">{formatCurrency(profile.intended_capital)}</span>. Units will recalculate automatically when the bot goes live.</p>
              )}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
            <StatCard title={isPaper ? "Paper Allocation" : "Total Invested"} value={formatCurrency(netInvested)} />
            <StatCard title="Your Portfolio Value" value={formatCurrency(currentValue)} color={currentValue >= netInvested ? 'text-profit' : 'text-loss'} />
            <StatCard title="Total Return" value={`${totalReturn >= 0 ? '+' : ''}${formatCurrency(totalReturn)} (${returnPct >= 0 ? '+' : ''}${returnPct.toFixed(1)}%)`} color={totalReturn >= 0 ? 'text-profit' : 'text-loss'} />
            <StatCard title="Fund Ownership" value={`${ownershipPct.toFixed(1)}%`} />
          </div>

          <div className="flex justify-between items-center mb-3">
            <h2 className="text-lg font-semibold">Capital History</h2>
            <div className="flex gap-2">
              <button onClick={() => setAddCapitalOpen(!addCapitalOpen)} className="btn btn-primary">Add Capital</button>
              <ExportButton data={events} filename="my_capital_events" />
            </div>
          </div>

          {addCapitalOpen && (
            <div className="card mb-4 flex flex-wrap gap-3 items-center">
              <input type="number" step="0.01" placeholder="Amount" value={capitalAmount}
                onChange={e => setCapitalAmount(e.target.value)}
                className="input w-40" />
              <button onClick={handleAddCapital} className="btn btn-success">Submit</button>
              {capitalMsg && <p className="text-sm text-neutral">{capitalMsg}</p>}
            </div>
          )}

          {events.length === 0 ? (
            <div className="card text-center text-neutral py-8">No capital events yet</div>
          ) : (
            <div className="table-scroll">
              <table className="w-full text-sm">
                <thead><tr className="border-b border-border">
                  <th className="text-left text-neutral py-2 px-2">Date</th>
                  <th className="text-left text-neutral py-2 px-2">Type</th>
                  <th className="text-right text-neutral py-2 px-2">Amount</th>
                  <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Units</th>
                  <th className="text-right text-neutral py-2 px-2 hidden md:table-cell">Ownership</th>
                </tr></thead>
                <tbody>
                  {events.map((e, i) => (
                    <tr key={i} className="border-b border-border">
                      <td className="py-2 px-2">{e.date}</td>
                      <td className="py-2 px-2">{e.event_type}</td>
                      <td className="py-2 px-2 text-right">{formatCurrency(e.amount)}</td>
                      <td className="py-2 px-2 text-right hidden md:table-cell">{parseFloat(e.units_assigned || 0).toFixed(2)}</td>
                      <td className="py-2 px-2 text-right hidden md:table-cell">{parseFloat(e.ownership_pct_after || 0).toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
