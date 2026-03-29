import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })
  const { marketSlug } = req.body
  if (!marketSlug) return res.status(400).json({ error: 'Missing marketSlug' })

  await supabase.from('market_mappings').update({ mapping_status: 'UNCONFIRMED' }).eq('polymarket_slug', marketSlug)
  res.status(200).json({ success: true })
}
