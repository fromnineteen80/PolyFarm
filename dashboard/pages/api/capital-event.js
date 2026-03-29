import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  const { first_name, last_name, email, event_type, date, amount, notes } = req.body
  if (!first_name || !last_name || !event_type || !amount) {
    return res.status(400).json({ error: 'Missing required fields' })
  }

  const amt = parseFloat(amount)
  if (isNaN(amt) || amt <= 0) return res.status(400).json({ error: 'Invalid amount' })

  // Get current wallet value
  const { data: snapshots } = await supabase.from('daily_snapshots').select('wallet_value').order('date', { ascending: false }).limit(1)
  const walletValue = parseFloat(snapshots?.[0]?.wallet_value || 0)

  // Get total units
  const { data: unitsCfg } = await supabase.from('bot_config').select('value').eq('key', 'total_units_outstanding')
  let totalUnits = parseFloat(unitsCfg?.[0]?.value || 0)

  // Check if first deposit ever
  const { data: existingEvents } = await supabase.from('capital_events').select('id').limit(1)
  const isFirstDeposit = !existingEvents || existingEvents.length === 0

  let unitsAssigned = 0
  if (event_type === 'withdrawal') {
    unitsAssigned = walletValue > 0 ? (amt / walletValue) * totalUnits : 0
    totalUnits -= unitsAssigned
  } else {
    if (isFirstDeposit) {
      unitsAssigned = 1000
      totalUnits = 1000
    } else {
      unitsAssigned = walletValue > 0 ? (amt / walletValue) * totalUnits : 0
      totalUnits += unitsAssigned
    }
  }

  // Upsert investor
  const { data: existing } = await supabase.from('investors').select('*').eq('first_name', first_name).eq('last_name', last_name).limit(1)
  let investor = existing?.[0]
  if (investor) {
    const newUnits = event_type === 'withdrawal'
      ? parseFloat(investor.units_held || 0) - unitsAssigned
      : parseFloat(investor.units_held || 0) + unitsAssigned
    await supabase.from('investors').update({ units_held: newUnits, email: email || investor.email }).eq('id', investor.id)
  } else {
    await supabase.from('investors').insert({ first_name, last_name, email, created_date: date, units_held: unitsAssigned, is_active: true })
  }

  // Update total units
  await supabase.from('bot_config').upsert({ key: 'total_units_outstanding', value: String(totalUnits), updated: new Date().toISOString() })

  // Insert capital event
  const ownershipAfter = totalUnits > 0 ? ((event_type === 'withdrawal' ? parseFloat(investor?.units_held || 0) - unitsAssigned : parseFloat(investor?.units_held || 0) + unitsAssigned) / totalUnits) * 100 : 100
  await supabase.from('capital_events').insert({
    timestamp: new Date().toISOString(), event_type, first_name, last_name, date, amount: amt,
    units_assigned: unitsAssigned, ownership_pct_after: ownershipAfter, wallet_value_at_event: walletValue, notes,
  })

  res.status(200).json({ success: true, unitsAssigned, totalUnits, ownershipAfter })
}
