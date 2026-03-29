import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

export async function uploadProfilePhoto(file, email) {
  const ext = file.name.split('.').pop()
  const filename = email.replace('@', '_').replace(/\./g, '_') + '.' + ext
  const { data, error } = await supabase
    .storage
    .from('profile-photos')
    .upload(filename, file, {
      upsert: true,
      contentType: file.type
    })
  if (error) throw error
  const { data: urlData } = supabase
    .storage
    .from('profile-photos')
    .getPublicUrl(filename)
  return urlData.publicUrl
}

export default supabase
