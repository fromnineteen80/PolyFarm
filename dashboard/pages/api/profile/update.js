import { getServerSession } from 'next-auth/next'
import { authOptions } from '../auth/[...nextauth]'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  const session = await getServerSession(req, res, authOptions)
  if (!session) return res.status(401).json({ error: 'Unauthorized' })

  const email = session.user.email
  const { first_name, last_name, display_name, profile_photo_url } = req.body

  const updates = {}
  if (first_name) updates.first_name = first_name
  if (last_name) updates.last_name = last_name
  if (display_name !== undefined) updates.display_name = display_name
  if (profile_photo_url !== undefined) updates.profile_photo_url = profile_photo_url
  updates.updated_at = new Date().toISOString()

  const { data, error } = await supabase
    .from('investor_profiles')
    .update(updates)
    .eq('email', email)
    .select()
    .single()

  if (error) return res.status(500).json({ error: error.message })

  // Also update investors table
  const investorUpdates = {}
  if (first_name) investorUpdates.first_name = first_name
  if (last_name) investorUpdates.last_name = last_name
  if (display_name !== undefined) investorUpdates.display_name = display_name
  if (profile_photo_url !== undefined) investorUpdates.profile_photo_url = profile_photo_url

  await supabase
    .from('investors')
    .update(investorUpdates)
    .eq('email', email)

  res.status(200).json({ success: true, profile: data })
}
