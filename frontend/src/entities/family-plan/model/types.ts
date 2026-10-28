// Типы семейного финансового плана

export interface Obligation {
  id: number
  groupId: number
  name: string
  description?: string
  amountRub: number
  dueDate: string       // ISO string
  isRecurring: boolean
  recurringDay?: number
  responsibleUserId: number
  responsibleUserName: string
  status: 'pending' | 'paid' | 'overdue' | 'cancelled'
  paidAt?: string
  createdBy: number
  createdAt: string
}

export interface Contribution {
  id: number
  groupId: number
  contributorUserId: number
  contributorName: string
  amountRub: number
  expectedDate: string
  note?: string
  status: 'proposed' | 'confirmed' | 'cancelled'
  confirmedBy?: number
  confirmedByName?: string
  received: boolean
  receivedAt?: string
  createdAt: string
}

export interface SharedResource {
  id: number
  userId: number
  userName: string
  resourceType: 'account' | 'fixed_amount'
  bankClientId?: number
  bankAccountId?: string
  fixedAmountRub?: number
  visibility: 'balance_only' | 'none'
  isActive: boolean
}

export interface DayBalance {
  date: string
  planned_balance: number
  events: Array<{
    type: 'obligation' | 'contribution'
    id: number
    name?: string
    amount_rub: number
    responsible_user_id?: number
    contributor_user_id?: number
    status?: string
  }>
  is_risk: boolean
}

export interface Forecast {
  included_balance_rub: number
  total_obligations_rub: number
  total_contributions_rub: number
  reserve_rub: number
  first_risk_date?: string
  min_balance_rub: number
  days: DayBalance[]
  data_as_of: string
  disclaimer: string
}

// ─── Request types ────────────────────────────────────────────────────────────

export interface ObligationCreateRequest {
  name: string
  description?: string
  amount_rub: number
  due_date: string
  responsible_user_id: number
  is_recurring?: boolean
  recurring_day?: number
}

export interface ContributionCreateRequest {
  amount_rub: number
  expected_date: string
  note?: string
}

export interface SharedResourceCreateRequest {
  resource_type: 'account' | 'fixed_amount'
  bank_client_id?: number
  bank_account_id?: string
  fixed_amount_kopecks?: number
  visibility?: 'balance_only' | 'none'
}
