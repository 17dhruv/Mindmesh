// Middleware temporarily disabled - using client-side auth checks only
// This is because Supabase v2 uses localStorage for auth, which isn't accessible in server-side middleware

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  // Just pass through - auth is handled client-side
  return NextResponse.next()
}

export const config = {
  matcher: [],
}

