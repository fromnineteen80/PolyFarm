import { getServerSession } from 'next-auth/next'
import { authOptions } from '../auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  const session = await getServerSession(req, res, authOptions)
  if (!session) return res.status(401).json({ error: 'Unauthorized' })

  // Recalculate all investor units from paper allocations
  // to real intended_capital amounts.
  //
  // Logic:
  //   1. Get all investor profiles with intended_capital
  //   2. First investor gets 1000 base units
  //   3. Each subsequent investor gets units proportional
  //      to their intended_capital relative to the running
  //      total wallet value at time of their deposit
  //   4. Since all deposits happen "at once" during go-live,
  //      we treat it as simultaneous: units = (intended / total_intended) * 1000 per investor
  //   5. Update investors table, capital_events, and total_units

  const { data: profiles } = await supabase
    .from('investor_profiles')
    .select('*')
    .eq('is_active', true)
    .order('created_at', { ascending: true })

  if (!profiles || profiles.length === 0) {
    return res.status(400).json({ error: 'No investor profiles found' })
  }

  // Calculate total intended capital across all investors
  const totalIntended = profiles.reduce(
    (s, p) => s + parseFloat(p.intended_capital || p.initial_capital || 0), 0
  )

  if (totalIntended <= 0) {
    return res.status(400).json({ error: 'No intended capital recorded' })
  }

  // Base units = 1000 per first investor, proportional for rest
  // Simplest fair method: each investor's units = (their_capital / total_capital) * 1000 * num_investors
  // This gives proportional ownership from day one
  const BASE_UNITS = 1000
  const totalUnits = BASE_UNITS * profiles.length
  const results = []

  for (const profile of profiles) {
    const intended = parseFloat(profile.intended_capital || profile.initial_capital || 0)
    const units = totalIntended > 0 ? (intended / totalIntended) * totalUnits : 0
    const ownershipPct = totalUnits > 0 ? (units / totalUnits) * 100 : 0

    // Update investors table
    await supabase
      .from('investors')
      .update({ units_held: units })
      .eq('email', profile.email)

    // Update investor profile with real capital
    await supabase
      .from('investor_profiles')
      .update({ initial_capital: intended })
      .eq('email', profile.email)

    // Insert go-live capital event
    await supabase.from('capital_events').insert({
      timestamp: new Date().toISOString(),
      event_type: 'go_live_adjustment',
      first_name: profile.first_name,
      last_name: profile.last_name,
      date: new Date().toISOString().split('T')[0],
      amount: intended,
      units_assigned: units,
      ownership_pct_after: ownershipPct,
      wallet_value_at_event: totalIntended,
      notes: `Go-live recalculation from paper (was $${parseFloat(profile.initial_capital || 0).toFixed(2)} paper)`,
    })

    results.push({
      email: profile.email,
      name: `${profile.first_name} ${profile.last_name}`,
      intended,
      units,
      ownershipPct,
    })
  }

  // Update total units in bot_config
  await supabase.from('bot_config').upsert({
    key: 'total_units_outstanding',
    value: String(totalUnits),
    updated: new Date().toISOString(),
  })

  res.status(200).json({ success: true, totalUnits, totalIntended, investors: results })
}
