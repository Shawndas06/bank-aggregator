export const API_BASE_URL = 'http://localhost:8000'

export const ROUTES = {
  HOME: '/',
  SIGN_IN: '/sign-in',
  SIGN_UP: '/sign-up',
  VERIFY_EMAIL: '/verify-email',
  DASHBOARD: '/dashboard',
  ACCOUNTS: '/accounts',
  GROUPS: '/groups',
  PROFILE: '/profile',
  PREMIUM: '/premium',
} as const

export const BANK_NAMES = {
  1: 'VBank',
  2: 'SBank',
  3: 'ABank',
} as const

export const AVAILABLE_BANKS = [
  { id: 1, name: 'vbank', displayName: 'VBank', color: 'from-blue-500 to-blue-600' },
  { id: 2, name: 'sbank', displayName: 'SBank', color: 'from-green-500 to-green-600' },
  { id: 3, name: 'abank', displayName: 'ABank', color: 'from-red-500 to-red-600' },
] as const

export const ACCOUNT_TYPES = {
  FREE: 'free',
  PREMIUM: 'premium',
} as const
