import { signIn } from 'next-auth/react'

export default function SignIn() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="card max-w-sm w-full text-center">
        <h1 className="text-2xl font-bold mb-2">OracleFarming</h1>
        <p className="text-neutral text-sm mb-6">Automated Sports Prediction Market Bot</p>
        <button onClick={() => signIn('google', { callbackUrl: '/' })} className="btn btn-signin">
          Sign in with Google
        </button>
      </div>
    </div>
  )
}
