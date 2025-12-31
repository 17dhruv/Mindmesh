import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function GET(req: NextRequest) {
  const reqUrl = new URL(req.url)
  const code = reqUrl.searchParams.get('code')
  const tokenHash = reqUrl.searchParams.get('token_hash')
  const type = reqUrl.searchParams.get('type')
  const error = reqUrl.searchParams.get('error')
  const errorDescription = reqUrl.searchParams.get('error_description')

  // Handle errors from Supabase
  if (error) {
    console.error('Auth error:', error, errorDescription)
    return NextResponse.redirect(
      new URL(`/auth/login?error=${error}&message=${encodeURIComponent(errorDescription || 'Authentication failed')}`, req.url)
    )
  }

  const cookieStore = cookies()
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: any) {
          cookieStore.set({ name, value, ...options })
        },
        remove(name: string, options: any) {
          cookieStore.set({ name, value: '', ...options })
        },
      },
    }
  )

  // Handle email verification or magic link
  if (type === 'email' || type === 'signup' || type === 'recovery') {
    if (tokenHash) {
      const { data, error: verifyError } = await supabase.auth.verifyOtp({
        token_hash: tokenHash,
        type: type as 'email' | 'signup' | 'recovery',
      })

      if (!verifyError && data.user) {
        // Successfully verified, redirect to dashboard
        return NextResponse.redirect(new URL('/dashboard', req.url))
      } else if (verifyError) {
        console.error('Verification error:', verifyError)
      }
    }
  }

  // Handle OAuth code exchange
  if (code) {
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Check if user has a session after verification
  const { data: { session } } = await supabase.auth.getSession()

  if (session) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  // No session, redirect to login with a message
  return NextResponse.redirect(
    new URL('/auth/login?message=Please login with your credentials', req.url)
  )
}
