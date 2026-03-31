import Link from 'next/link'
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import supabase from '../lib/supabase'
import { formatCurrency, calcInvestorValue } from '../lib/calculations'
import Icon from './Icon'

const NAV_LINKS = [
  { href: '/', label: 'Today' },
  { href: '/performance', label: 'Performance' },
  { href: '/analytics', label: 'Analytics' },
  { href: '/research', label: 'Research' },
  { href: '/investors', label: 'Investors' },
  { href: '/about', label: 'About' },
]

export default function NavBar() {
  const router = useRouter()
  const { data: session } = useSession()
  const [menuOpen, setMenuOpen] = useState(false)
  const [investorData, setInvestorData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      if (!session?.user?.email) { setLoading(false); return }
      try {
        const email = session.user.email
        const [invRes, cfgRes, snapRes] = await Promise.all([
          supabase.from('investors').select('units_held').eq('email', email).maybeSingle(),
          supabase.from('bot_config').select('value').eq('key', 'total_units_outstanding'),
          supabase.from('daily_snapshots').select('wallet_value,date').order('date', { ascending: false }).limit(2),
        ])

        const units = parseFloat(invRes.data?.units_held || 0)
        const totalUnits = parseFloat(cfgRes.data?.[0]?.value || 0)
        const todayWallet = parseFloat(snapRes.data?.[0]?.wallet_value || 0)
        const yesterdayWallet = parseFloat(snapRes.data?.[1]?.wallet_value || todayWallet)

        const todayValue = calcInvestorValue(units, totalUnits, todayWallet)
        const yesterdayValue = calcInvestorValue(units, totalUnits, yesterdayWallet)
        const dailyPnl = todayValue - yesterdayValue

        const { data: events } = await supabase
          .from('capital_events')
          .select('amount,event_type')
          .eq('first_name', session.user.profile?.first_name || '')

        const totalInvested = (events || [])
          .filter(e => e.event_type !== 'withdrawal')
          .reduce((s, e) => s + parseFloat(e.amount || 0), 0)

        setInvestorData({ units, totalUnits, todayValue, dailyPnl, totalInvested })
      } catch (err) {}
      setLoading(false)
    }
    load()
    const interval = setInterval(load, 30000)
    return () => clearInterval(interval)
  }, [session])

  const profilePhoto = session?.user?.profile?.profile_photo_url
  const initial = (session?.user?.profile?.first_name || session?.user?.name || '?')[0]?.toUpperCase()

  return (
    <nav className="bg-surface border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <div className="flex items-center gap-6">
          <Link href="/" className="text-lg font-bold text-white min-h-[44px] flex items-center">OracleFarming</Link>
          <div className="hidden md:flex gap-1">
            {NAV_LINKS.map(l => (
              <Link key={l.href} href={l.href}
                className={`px-3 py-1 text-sm rounded min-h-[44px] flex items-center ${router.pathname === l.href || (l.href !== '/' && router.pathname.startsWith(l.href)) ? 'text-profit font-semibold' : 'text-neutral hover:text-white'}`}>
                {l.label}
              </Link>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center gap-4 text-sm">
            {loading ? (
              <div className="flex gap-3">
                <span className="skeleton h-4 w-16" />
                <span className="skeleton h-4 w-16" />
              </div>
            ) : investorData ? (
              <>
                <div>
                  <span className="text-xs text-neutral mr-1">Value</span>
                  <span className="font-semibold">{formatCurrency(investorData.todayValue)}</span>
                </div>
                <div>
                  <span className="text-xs text-neutral mr-1">Today</span>
                  <span className={`font-bold ${investorData.dailyPnl >= 0 ? 'text-profit' : 'text-loss'}`}>
                    {investorData.dailyPnl >= 0 ? '+' : ''}{formatCurrency(investorData.dailyPnl)}
                  </span>
                </div>
              </>
            ) : null}
          </div>

          <Link href="/profile" className="flex items-center min-h-[44px] min-w-[44px] justify-center">
            <div className="w-10 h-10 rounded-full border-2 border-border hover:border-profit transition overflow-hidden flex items-center justify-center bg-surface">
              {profilePhoto ? (
                <img src={profilePhoto} alt="Profile" className="w-full h-full object-cover" />
              ) : (
                <span className="text-sm font-bold text-neutral">{initial}</span>
              )}
            </div>
          </Link>

          <button onClick={() => setMenuOpen(!menuOpen)} className="btn md:hidden p-2">
            <Icon name={menuOpen ? 'close' : 'menu'} />
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="md:hidden border-t border-border px-4 py-2">
          {NAV_LINKS.map(l => (
            <Link key={l.href} href={l.href} onClick={() => setMenuOpen(false)}
              className={`block py-2 text-sm min-h-[44px] flex items-center ${router.pathname === l.href ? 'text-profit' : 'text-neutral'}`}>
              {l.label}
            </Link>
          ))}
          <Link href="/profile" onClick={() => setMenuOpen(false)}
            className="block py-2 text-sm min-h-[44px] flex items-center text-neutral">
            Profile
          </Link>
        </div>
      )}
    </nav>
  )
}
