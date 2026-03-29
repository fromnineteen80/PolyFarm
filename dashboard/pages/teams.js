import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'
import Layout from '../components/Layout'
import StatCard from '../components/StatCard'
import { formatCurrency } from '../lib/calculations'
import { useState } from 'react'

// Hardcoded from bot config — dashboard reads from bot_config if available
const DOMINANT_TEAMS = {
  "Chicago Bulls": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.28, deficit_range: [5, 15], market_overreaction_tendency: "high", notes: "League leader in 10+ point comeback wins 2024-25" },
  "Indiana Pacers": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.32, deficit_range: [5, 15], market_overreaction_tendency: "high", notes: "12 wins from 15+ down in 2024-25 — NBA record" },
  "Oklahoma City Thunder": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.36, deficit_range: [5, 12], market_overreaction_tendency: "high", notes: "SGA MVP. Best team in NBA 2025-26." },
  "Denver Nuggets": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.37, deficit_range: [5, 12], market_overreaction_tendency: "high", notes: "Jokic efficiency. Home altitude advantage." },
  "Boston Celtics": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.35, deficit_range: [5, 15], market_overreaction_tendency: "very_high", notes: "Championship experience. Market overreacts to deficits." },
  "Golden State Warriors": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.34, deficit_range: [5, 15], market_overreaction_tendency: "very_high", notes: "Curry three-point runs erase deficits rapidly." },
  "Cleveland Cavaliers": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.35, deficit_range: [5, 12], market_overreaction_tendency: "medium", notes: "Best East record. Garland clutch play." },
  "Los Angeles Lakers": { sport: "basketball_nba", comeback_win_rate_when_trailing: 0.33, deficit_range: [5, 15], market_overreaction_tendency: "high", notes: "LeBron and Davis late game execution." },
  "Los Angeles Dodgers": { sport: "baseball_mlb", comeback_win_rate_when_trailing: 0.36, deficit_range: [1, 3], market_overreaction_tendency: "very_high", notes: "Primary MLB target. Deepest lineup in baseball." },
  "New York Yankees": { sport: "baseball_mlb", comeback_win_rate_when_trailing: 0.33, deficit_range: [1, 3], market_overreaction_tendency: "high", notes: "Historical comeback machine. High market volume." },
  "Houston Astros": { sport: "baseball_mlb", comeback_win_rate_when_trailing: 0.30, deficit_range: [1, 2], market_overreaction_tendency: "medium", notes: "Elite process. Best late-inning manufacturing." },
  "Philadelphia Phillies": { sport: "baseball_mlb", comeback_win_rate_when_trailing: 0.29, deficit_range: [1, 2], market_overreaction_tendency: "medium", notes: "Citizens Bank Park hitter-friendly. Power upside." },
  "Colorado Avalanche": { sport: "icehockey_nhl", comeback_win_rate_when_trailing: 0.34, deficit_range: [1, 2], market_overreaction_tendency: "high", notes: "MacKinnon effect. Elite power play when trailing." },
  "Edmonton Oilers": { sport: "icehockey_nhl", comeback_win_rate_when_trailing: 0.35, deficit_range: [1, 2], market_overreaction_tendency: "very_high", notes: "McDavid and Draisaitl. Most dangerous trailing pair in NHL." },
  "Dallas Stars": { sport: "icehockey_nhl", comeback_win_rate_when_trailing: 0.31, deficit_range: [1, 2], market_overreaction_tendency: "medium", notes: "Elite defensive structure with explosive offense." },
  "Kansas City Chiefs": { sport: "americanfootball_nfl", comeback_win_rate_when_trailing: 0.44, deficit_range: [3, 14], market_overreaction_tendency: "very_high", notes: "Mahomes effect. Single best exception signal in all sports." },
  "San Francisco 49ers": { sport: "americanfootball_nfl", comeback_win_rate_when_trailing: 0.38, deficit_range: [3, 14], market_overreaction_tendency: "high", notes: "Shanahan system. Second half trailing strength." },
  "Chicago Bears": { sport: "americanfootball_nfl", comeback_win_rate_when_trailing: 0.28, deficit_range: [3, 10], market_overreaction_tendency: "medium", notes: "Caleb Williams Year 2. Bot accumulates live data to confirm." },
  "Duke Blue Devils": { sport: "basketball_ncaab", comeback_win_rate_when_trailing: 0.38, deficit_range: [5, 15], market_overreaction_tendency: "very_high", notes: "Brand effect. Cameron Indoor. Market overprices deficits." },
  "Kansas Jayhawks": { sport: "basketball_ncaab", comeback_win_rate_when_trailing: 0.36, deficit_range: [5, 15], market_overreaction_tendency: "high", notes: "Allen Fieldhouse. Home comeback rate exceptional." },
  "Kentucky Wildcats": { sport: "basketball_ncaab", comeback_win_rate_when_trailing: 0.35, deficit_range: [5, 12], market_overreaction_tendency: "high", notes: "Rupp Arena home court. Blue blood program." },
  "Connecticut Huskies": { sport: "basketball_ncaab", comeback_win_rate_when_trailing: 0.37, deficit_range: [5, 12], market_overreaction_tendency: "high", notes: "Back-to-back champions. Hurley coaching documented." },
  "Manchester City": { sport: "soccer_epl", comeback_win_rate_when_trailing: 0.29, deficit_range: [1, 1], market_overreaction_tendency: "high", notes: "Guardiola adjustments. One goal deficit only." },
  "Arsenal": { sport: "soccer_epl", comeback_win_rate_when_trailing: 0.27, deficit_range: [1, 1], market_overreaction_tendency: "medium", notes: "Emirates home matches strongest signal." },
  "Los Angeles FC": { sport: "soccer_usa_mls", comeback_win_rate_when_trailing: 0.26, deficit_range: [1, 1], market_overreaction_tendency: "medium", notes: "Best MLS team. Markets less efficient — bigger gaps." },
}

const FADE_TEAMS = {
  "Pittsburgh Pirates": { sport: "baseball_mlb", confidence: "very_high", reason: "Chronically thin roster. Market prices hope that never materializes." },
  "Chicago White Sox": { sport: "baseball_mlb", confidence: "very_high", reason: "101-223 combined record 2024-25. Historically bad." },
  "Utah Jazz": { sport: "basketball_nba", confidence: "very_high", reason: "20-47. Worst defense in NBA. 30th DRTG. Tanking." },
  "Brooklyn Nets": { sport: "basketball_nba", confidence: "very_high", reason: "Worst clutch record in entire NBA 2025-26." },
  "Vancouver Canucks": { sport: "icehockey_nhl", confidence: "very_high", reason: "21-40-8. Worst team in NHL. Minus-84 goal diff." },
  "New York Rangers": { sport: "icehockey_nhl", confidence: "very_high", reason: "First team eliminated from playoffs in East. 29-35-9." },
  "New York Jets": { sport: "americanfootball_nfl", confidence: "very_high", reason: "3-14 record. Organizational dysfunction." },
  "Tennessee Titans": { sport: "americanfootball_nfl", confidence: "very_high", reason: "3-14 record. Rebuilding." },
  "Milwaukee Brewers": { sport: "baseball_mlb", confidence: "high", reason: "Pitching dependent. Offense cannot manufacture late runs." },
  "Cleveland Guardians": { sport: "baseball_mlb", confidence: "high", reason: "Contact-heavy, no power." },
  "Oakland Athletics": { sport: "baseball_mlb", confidence: "high", reason: "Rebuilding. Minimal talent." },
  "Colorado Rockies": { sport: "baseball_mlb", confidence: "high", reason: "Coors Field misleads market on road/pitching matchups." },
  "Washington Wizards": { sport: "basketball_nba", confidence: "high", reason: "Bottom two team in league." },
  "Sacramento Kings": { sport: "basketball_nba", confidence: "high", reason: "29th net rating despite recognizable names." },
  "San Jose Sharks": { sport: "icehockey_nhl", confidence: "high", reason: "Multi-year rebuild." },
  "Chicago Blackhawks": { sport: "icehockey_nhl", confidence: "high", reason: "Multi-year rebuild. Bedard developing." },
  "Las Vegas Raiders": { sport: "americanfootball_nfl", confidence: "high", reason: "2-14 last season. Organizational chaos." },
  "Arizona Cardinals": { sport: "americanfootball_nfl", confidence: "high", reason: "3-14 record. Bottom-three comeback efficiency." },
  "Miami Marlins": { sport: "baseball_mlb", confidence: "medium", reason: "Rebuild. Thin bullpen depth when trailing late." },
  "Texas Rangers": { sport: "baseball_mlb", confidence: "medium", reason: "Roster collapse post-championship." },
  "Charlotte Hornets": { sport: "basketball_nba", confidence: "medium", reason: "Consistent bottom-five team." },
  "Winnipeg Jets": { sport: "icehockey_nhl", confidence: "medium", reason: "Won Presidents Trophy last season. Now 30-30-12." },
  "Carolina Panthers": { sport: "americanfootball_nfl", confidence: "medium", reason: "Multi-year rebuild." },
}

const TENDENCY_COLORS = { very_high: 'bg-profit text-black', high: 'bg-bandA text-black', medium: 'bg-paper text-black', low: 'bg-neutral text-white' }
const CONFIDENCE_COLORS = { very_high: 'bg-profit text-black', high: 'bg-bandA text-black', medium: 'bg-paper text-black' }
const SPORT_LABELS = { basketball_nba: 'NBA', icehockey_nhl: 'NHL', baseball_mlb: 'MLB', basketball_ncaab: 'NCAAB', americanfootball_nfl: 'NFL', soccer_epl: 'EPL', soccer_usa_mls: 'MLS' }

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) return { redirect: { destination: '/auth/signin', permanent: false } }
  if (!session.user.hasProfile) return { redirect: { destination: '/profile/setup', permanent: false } }
  const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  const { data: trades } = await sb.from('trades').select('position_type,fade_team,exception_trigger_reason,pnl,sport,raw_edge_at_entry,hold_duration_seconds').not('timestamp_exit', 'is', null)
  return { props: { session, trades: trades || [] } }
}

export default function Teams({ trades }) {
  const [sportFilter, setSportFilter] = useState('')

  // Build team performance from trades
  const teamPerf = {}
  trades.forEach(t => {
    let team = null
    if (t.position_type === 'exception' && t.exception_trigger_reason) {
      const match = Object.keys(DOMINANT_TEAMS).find(tn => t.exception_trigger_reason?.includes(tn))
      if (match) team = match
    }
    if (t.position_type === 'fade' && t.fade_team) team = t.fade_team
    if (!team) return
    if (!teamPerf[team]) teamPerf[team] = { trades: 0, wins: 0, pnl: 0, totalEdge: 0, totalHold: 0 }
    teamPerf[team].trades++
    if (parseFloat(t.pnl || 0) > 0) teamPerf[team].wins++
    teamPerf[team].pnl += parseFloat(t.pnl || 0)
    teamPerf[team].totalEdge += parseFloat(t.raw_edge_at_entry || 0)
    teamPerf[team].totalHold += parseInt(t.hold_duration_seconds || 0)
  })

  const allSports = [...new Set([...Object.values(DOMINANT_TEAMS).map(t => t.sport), ...Object.values(FADE_TEAMS).map(t => t.sport)])]

  const renderTeamCard = (name, config, type) => {
    if (sportFilter && config.sport !== sportFilter) return null
    const perf = teamPerf[name]
    const tendency = type === 'dominant' ? config.market_overreaction_tendency : config.confidence
    const tendencyColor = type === 'dominant' ? TENDENCY_COLORS[tendency] : CONFIDENCE_COLORS[tendency]

    let confidenceScore = null
    let confidenceColor = 'text-neutral'
    if (perf && perf.trades >= 5) {
      const actualWR = perf.wins / perf.trades
      const configWR = type === 'dominant' ? config.comeback_win_rate_when_trailing : 0.5
      confidenceScore = (actualWR * 0.6 + configWR * 0.4) * 100
    } else if (type === 'dominant') {
      confidenceScore = config.comeback_win_rate_when_trailing * 100
    }
    if (confidenceScore >= 80) confidenceColor = 'text-profit'
    else if (confidenceScore >= 60) confidenceColor = 'text-bandA'
    else if (confidenceScore) confidenceColor = 'text-paper'

    return (
      <div key={name} className="card">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-semibold">{name}</h3>
            <span className="text-xs text-neutral">{SPORT_LABELS[config.sport] || config.sport}</span>
          </div>
          <span className={`text-xs px-2 py-0.5 rounded font-bold ${tendencyColor || 'bg-neutral text-white'}`}>
            {(tendency || 'medium').toUpperCase().replace('_', ' ')}
          </span>
        </div>
        <p className="text-sm text-neutral mb-2">{type === 'dominant' ? config.notes : config.reason}</p>
        {type === 'dominant' && (
          <div className="text-xs text-neutral mb-2">
            <p>Comeback rate: {(config.comeback_win_rate_when_trailing * 100).toFixed(0)}%</p>
            <p>Exception at {config.deficit_range[0]}-{config.deficit_range[1]} deficit</p>
          </div>
        )}
        {perf ? (
          <div className="text-xs border-t border-border pt-2 mt-2">
            <p>Trades: {perf.trades} | WR: {(perf.wins / perf.trades * 100).toFixed(0)}% | P&L: {formatCurrency(perf.pnl)}</p>
            <p>Avg gap: {(perf.totalEdge / perf.trades * 100).toFixed(1)}¢ | Avg hold: {Math.round(perf.totalHold / perf.trades / 60)}m</p>
          </div>
        ) : (
          <p className="text-xs text-neutral border-t border-border pt-2 mt-2">Performance data accumulates as bot trades.</p>
        )}
        {confidenceScore && <p className={`text-xs mt-1 ${confidenceColor}`}>Confidence: {confidenceScore.toFixed(0)}%{perf && perf.trades < 5 ? ' (config)' : ''}</p>}
      </div>
    )
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Team Intelligence</h1>
      <div className="flex flex-wrap gap-2 mb-6">
        <button onClick={() => setSportFilter('')} className={`btn ${!sportFilter ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>All</button>
        {allSports.map(s => (
          <button key={s} onClick={() => setSportFilter(s)} className={`btn ${sportFilter === s ? 'btn-toggle-active' : 'btn-toggle-inactive'}`}>
            {SPORT_LABELS[s] || s}
          </button>
        ))}
      </div>

      <h2 className="text-lg font-semibold mb-3 text-profit">Dominant Teams (Exception Trades)</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3 mb-8">
        {Object.entries(DOMINANT_TEAMS).map(([name, cfg]) => renderTeamCard(name, cfg, 'dominant'))}
      </div>

      <h2 className="text-lg font-semibold mb-3 text-loss">Fade Teams (Bet Against)</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
        {Object.entries(FADE_TEAMS).map(([name, cfg]) => renderTeamCard(name, cfg, 'fade'))}
      </div>
    </Layout>
  )
}
