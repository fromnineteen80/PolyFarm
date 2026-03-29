import { getServerSession } from 'next-auth/next'
import { authOptions } from '../auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  const session = await getServerSession(req, res, authOptions)
  if (!session) return res.status(401).json({ error: 'Unauthorized' })

  const email = session.user.email
  const { first_name, last_name, display_name, profile_photo_url, initial_capital } = req.body

  if (!first_name || !last_name) {
    return res.status(400).json({ error: 'First name and last name are required' })
  }

  const amount = parseFloat(initial_capital || 0)
  if (amount < 0) return res.status(400).json({ error: 'Invalid capital amount' })

  // Check if profile already exists
  const { data: existing } = await supabase
    .from('investor_profiles')
    .select('id')
    .eq('email', email)
    .single()

  if (existing) return res.status(409).json({ error: 'Profile already exists' })

  // Create investor profile
  const { data: profile, error: profileError } = await supabase
    .from('investor_profiles')
    .insert({
      email,
      first_name,
      last_name,
      display_name: display_name || `${first_name} ${last_name}`,
      profile_photo_url: profile_photo_url || null,
      initial_capital: amount,
      joined_date: new Date().toISOString().split('T')[0],
    })
    .select()
    .single()

  if (profileError) return res.status(500).json({ error: profileError.message })

  // Create or update investors record
  const { data: inv } = await supabase
    .from('investors')
    .select('*')
    .eq('email', email)
    .single()

  if (!inv) {
    await supabase.from('investors').insert({
      first_name,
      last_name,
      email,
      display_name: display_name || `${first_name} ${last_name}`,
      profile_photo_url: profile_photo_url || null,
      created_date: new Date().toISOString().split('T')[0],
      units_held: 0,
      is_active: true,
    })
  }

  // Record initial capital event if amount > 0
  if (amount > 0) {
    const { data: snapshots } = await supabase
      .from('daily_snapshots')
      .select('wallet_value')
      .order('date', { ascending: false })
      .limit(1)
    const walletValue = parseFloat(snapshots?.[0]?.wallet_value || 0)

    const { data: unitsCfg } = await supabase
      .from('bot_config')
      .select('value')
      .eq('key', 'total_units_outstanding')
    let totalUnits = parseFloat(unitsCfg?.[0]?.value || 0)

    const { data: existingEvents } = await supabase
      .from('capital_events')
      .select('id')
      .limit(1)
    const isFirstDeposit = !existingEvents || existingEvents.length === 0

    let unitsAssigned = 0
    if (isFirstDeposit) {
      unitsAssigned = 1000
      totalUnits = 1000
    } else {
      unitsAssigned = walletValue > 0 ? (amount / walletValue) * totalUnits : 0
      totalUnits += unitsAssigned
    }

    // Update investor units
    await supabase
      .from('investors')
      .update({ units_held: unitsAssigned })
      .eq('email', email)

    // Update total units
    await supabase.from('bot_config').upsert({
      key: 'total_units_outstanding',
      value: String(totalUnits),
      updated: new Date().toISOString(),
    })

    // Insert capital event
    const ownershipAfter = totalUnits > 0 ? (unitsAssigned / totalUnits) * 100 : 100
    await supabase.from('capital_events').insert({
      timestamp: new Date().toISOString(),
      event_type: 'initial',
      first_name,
      last_name,
      date: new Date().toISOString().split('T')[0],
      amount,
      units_assigned: unitsAssigned,
      ownership_pct_after: ownershipAfter,
      wallet_value_at_event: walletValue,
      notes: 'Initial deposit via profile setup',
    })
  }

  res.status(200).json({ success: true, profile })
}
