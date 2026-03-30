import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    })
  ],
  callbacks: {
    async signIn({ user }) {
      const allowed = (process.env.GOOGLE_AUTHORIZED_EMAILS || process.env.GOOGLE_AUTHORIZED_EMAIL || '')
        .split(',')
        .map(e => e.trim())
        .filter(Boolean)
      return allowed.includes(user.email)
    },
    async session({ session }) {
      if (!session?.user?.email) return session
      try {
        const { data } = await supabase
          .from('investor_profiles')
          .select('id, first_name, last_name, profile_photo_url, display_name')
          .eq('email', session.user.email)
          .maybeSingle()
        session.user.hasProfile = !!data
        session.user.profile = data || null
      } catch (e) {
        session.user.hasProfile = false
        session.user.profile = null
      }
      return session
    }
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
  secret: process.env.NEXTAUTH_SECRET,
}

export default NextAuth(authOptions)
