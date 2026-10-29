export type User = {
  email: string
  phone: string | null
  avatarUrl: string | null
  isVerified: boolean
  id: number
  name: string
  birthDate: string
  accountType: 'free' | 'premium'
}

export type AccountType = 'free' | 'premium'
