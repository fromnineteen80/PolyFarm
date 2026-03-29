import Link from 'next/link'
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import supabase from '../lib/supabase'
import { formatCurrency } from '../lib/calculations'

const NAV_LINKS = [
  { href: '/', label: 'Overview' },
  { href: '/projections', label: 'Projections' },
  { href: '/bands', label: 'Bands' },
  { href: '/daily', label: 'Daily' },
  { href: '/range', label: 'Range' },
  { href: '/investors', label: 'Investors' },
  { href: '/history', label: 'History' },
  { href: '/performance', label: 'Performance' },
  { href: '/sessions', label: 'Sessions' },
  { href: '/markets', label: 'Markets' },
  { href: '/mispricing', label: 'Mispricing' },
  { href: '/teams', label: 'Teams' },
]

export default function NavBar() {
  const router = useRouter()
  const [menuOpen, setMenuOpen] = useState(false)
  const [wallet, setWallet] = useState(null)
  const [mode, setMode] = useState('paper')

  useEffect(() => {
    async function load() {
      const { data: snap } = await supabase.from('daily_snapshots').select('wallet_value,session_pnl,paper_mode').order('date', { ascending: false }).limit(1)
      if (snap?.[0]) { setWallet(snap[0]); setMode(snap[0].paper_mode ? 'paper' : 'live') }
      const { data: cfg } = await supabase.from('bot_config').select('value').eq('key', 'current_mode')
      if (cfg?.[0]?.value) setMode(cfg[0].value)
    }
    load()
  }, [])

  return (
    <nav className="bg-surface border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-lg font-bold text-white min-h-[44px] flex items-center">PolyFarm</Link>
          <div className="hidden md:flex gap-1">
            {NAV_LINKS.map(l => (
              <Link key={l.href} href={l.href}
                className={`px-2 py-1 text-sm rounded min-h-[44px] flex items-center ${router.pathname === l.href ? 'text-profit font-semibold' : 'text-neutral hover:text-white'}`}>
                {l.label}
              </Link>
            ))}
          </div>
        </div>
        <div className="hidden md:flex items-center gap-3 text-sm font-financial">
          <span>Wallet: {formatCurrency(wallet?.wallet_value)}</span>
          <span className={parseFloat(wallet?.session_pnl || 0) >= 0 ? 'text-profit' : 'text-loss'}>
            Today: {parseFloat(wallet?.session_pnl || 0) >= 0 ? '+' : ''}{formatCurrency(wallet?.session_pnl)}
          </span>
          <span className={`px-2 py-0.5 rounded text-xs font-bold ${mode === 'live' ? 'bg-live text-black' : 'bg-paper text-black'}`}>
            {mode?.toUpperCase()}
          </span>
        </div>
        <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2 min-h-[44px]">
          <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={menuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'} />
          </svg>
        </button>
      </div>
      {menuOpen && (
        <div className="md:hidden border-t border-border px-4 py-2">
          {NAV_LINKS.map(l => (
            <Link key={l.href} href={l.href} onClick={() => setMenuOpen(false)}
              className={`block py-2 text-sm min-h-[44px] flex items-center ${router.pathname === l.href ? 'text-profit' : 'text-neutral'}`}>
              {l.label}
            </Link>
          ))}
          <div className="mt-2 pt-2 border-t border-border text-sm font-financial">
            <p>Wallet: {formatCurrency(wallet?.wallet_value)}</p>
            <span className={`px-2 py-0.5 rounded text-xs font-bold inline-block mt-1 ${mode === 'live' ? 'bg-live text-black' : 'bg-paper text-black'}`}>{mode?.toUpperCase()}</span>
          </div>
        </div>
      )}
    </nav>
  )
}
