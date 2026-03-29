import { SessionProvider } from "next-auth/react"
import { useEffect } from 'react'
import '../styles/globals.css'

export default function App({ Component, pageProps: { session, ...pageProps } }) {
  useEffect(() => {
    // Register Chart.js components client-side only
    import('../components/charts/ChartSetup')
  }, [])

  return (
    <SessionProvider session={session}>
      <Component {...pageProps} />
    </SessionProvider>
  )
}
