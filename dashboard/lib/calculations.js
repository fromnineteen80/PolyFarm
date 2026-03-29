import { differenceInDays, eachDayOfInterval, format } from 'date-fns'

export function calcProjection(startValue, startDate, ratePerDay) {
  const days = differenceInDays(new Date(), new Date(startDate))
  return startValue * Math.pow(1 + ratePerDay, Math.max(days, 0))
}

export function calcProjectionSeries(startValue, startDate, ratePerDay, endDate) {
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  if (start > end) return []
  const days = eachDayOfInterval({ start, end })
  return days.map((d, i) => ({
    date: format(d, 'yyyy-MM-dd'),
    value: startValue * Math.pow(1 + ratePerDay, i),
  }))
}

export function calcOwnershipUnits(depositAmount, walletValue, totalUnitsOutstanding) {
  if (walletValue <= 0) return 1000
  return (depositAmount / walletValue) * totalUnitsOutstanding
}

export function calcWithdrawalUnits(withdrawalAmount, walletValue, totalUnitsOutstanding) {
  if (walletValue <= 0) return 0
  return (withdrawalAmount / walletValue) * totalUnitsOutstanding
}

export function calcInvestorValue(investorUnits, totalUnits, walletValue) {
  if (totalUnits <= 0) return 0
  return (investorUnits / totalUnits) * walletValue
}

export function calcOwnershipPct(investorUnits, totalUnits) {
  if (totalUnits <= 0) return 0
  return (investorUnits / totalUnits) * 100
}

export function calcSharpe(dailyReturns) {
  if (!dailyReturns || dailyReturns.length < 2) return 0
  const DAILY_RISK_FREE = 0.05 / 365
  const avg = dailyReturns.reduce((a, b) => a + b, 0) / dailyReturns.length
  const variance = dailyReturns.reduce((sum, r) => sum + Math.pow(r - avg, 2), 0) / (dailyReturns.length - 1)
  const stddev = Math.sqrt(variance)
  if (stddev === 0) return 0
  return (avg - DAILY_RISK_FREE) / stddev
}

export function calcMaxDrawdown(walletHistory) {
  if (!walletHistory || walletHistory.length < 2) {
    return { maxDrawdown: 0, worstPeak: 0, worstTrough: 0 }
  }
  let peak = walletHistory[0]
  let maxDD = 0
  let worstPeak = peak
  let worstTrough = peak
  for (const val of walletHistory) {
    if (val > peak) peak = val
    const dd = (peak - val) / peak
    if (dd > maxDD) {
      maxDD = dd
      worstPeak = peak
      worstTrough = val
    }
  }
  return { maxDrawdown: maxDD, worstPeak, worstTrough }
}

export function calcRollingWinRate(trades, windowDays) {
  if (!trades || trades.length === 0) return []
  const sorted = [...trades].sort((a, b) => new Date(a.timestamp_entry) - new Date(b.timestamp_entry))
  const results = []
  for (let i = 0; i < sorted.length; i++) {
    const cutoff = new Date(sorted[i].timestamp_entry)
    cutoff.setDate(cutoff.getDate() - windowDays)
    const window = sorted.filter(t => {
      const d = new Date(t.timestamp_entry)
      return d >= cutoff && d <= new Date(sorted[i].timestamp_entry)
    })
    const wins = window.filter(t => parseFloat(t.pnl || 0) > 0).length
    results.push({
      date: sorted[i].timestamp_entry?.split('T')[0],
      winRate: window.length > 0 ? wins / window.length : 0,
    })
  }
  return results
}

export function formatCurrency(value) {
  if (value === null || value === undefined) return '$0.00'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

export function formatPct(value) {
  if (value === null || value === undefined) return '0.00%'
  return (value * 100).toFixed(2) + '%'
}
