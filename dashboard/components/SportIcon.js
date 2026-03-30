import Icon from './Icon'

const SPORT_ICONS = {
  basketball_nba: 'sports_basketball',
  basketball_ncaab: 'sports_basketball',
  americanfootball_nfl: 'sports_football',
  americanfootball_ncaaf: 'sports_football',
  baseball_mlb: 'sports_baseball',
  icehockey_nhl: 'sports_hockey',
  soccer_epl: 'sports_soccer',
  soccer_usa_mls: 'sports_soccer',
  soccer_mls: 'sports_soccer',
  soccer_germany_bundesliga: 'sports_soccer',
  soccer_spain_la_liga: 'sports_soccer',
  soccer_italy_serie_a: 'sports_soccer',
  soccer_france_ligue_1: 'sports_soccer',
  soccer_uefa_champions_league: 'sports_soccer',
  soccer_uefa_europa_league: 'sports_soccer',
}

const SPORT_LABELS = {
  basketball_nba: 'NBA',
  basketball_ncaab: 'NCAAB',
  americanfootball_nfl: 'NFL',
  americanfootball_ncaaf: 'NCAAF',
  baseball_mlb: 'MLB',
  icehockey_nhl: 'NHL',
  soccer_epl: 'EPL',
  soccer_usa_mls: 'MLS',
}

export default function SportIcon({ sport, showLabel, size }) {
  const icon = SPORT_ICONS[sport] || 'sports'
  const label = SPORT_LABELS[sport] || sport?.split('_').pop()?.toUpperCase() || ''
  return (
    <span className="inline-flex items-center gap-1">
      <Icon name={icon} size={size || 'sm'} />
      {showLabel && <span className="text-xs text-neutral">{label}</span>}
    </span>
  )
}

export { SPORT_ICONS, SPORT_LABELS }
