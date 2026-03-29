import { useRouter } from 'next/router'
import Link from 'next/link'

export default function AuthError() {
  const { query } = useRouter()
  const isAccessDenied = query.error === 'AccessDenied'

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="card max-w-sm w-full text-center">
        <h1 className="text-xl font-bold mb-4 text-loss">Access Denied</h1>
        {isAccessDenied ? (
          <p className="text-neutral text-sm mb-6">Only authorized accounts may access this dashboard.</p>
        ) : (
          <p className="text-neutral text-sm mb-6">An authentication error occurred: {query.error}</p>
        )}
        <Link href="/auth/signin" className="text-info hover:underline min-h-[44px] inline-flex items-center">
          Back to Sign In
        </Link>
      </div>
    </div>
  )
}
