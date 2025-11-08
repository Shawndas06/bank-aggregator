export type Account = {
  accountId: string
  clientId: number
  clientName: string
  accountName: string
  isActive: boolean
}

export type GroupAccount = {
  accountId: string
  clientId: string
  clientName: string
  accountName: string
  owner: {
    name: string
  }
}

export type Balance = {
  amount: number
  currency: string
}

export type TransactionType = 'debit' | 'credit'

export type Transaction = {
  id: string
  date: string
  description: string
  amount: number
  currency: string
  type: TransactionType
}
