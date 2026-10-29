export type AnalyticsOverview = {
  totalBalance: number
  accountsCount: number
  currentMonth: {
    expenses: number
    income: number
    expenseChange: number
    incomeChange: number
  }
  topCategories: Array<{
    category: string
    categoryName: string
    amount: number
    percentage: number
  }>
}

export type CategoryBreakdown = {
  category: string
  categoryName: string
  amount: number
  count: number
  percentage: number
}


export type InsightMessage = {
  type?: string
  title: string
  message: string
  action?: string
  icon?: string
}

export type AdvancedInsights = {
  metrics: {
    savingsRate: number
    avgDailyExpense: number
    avgDailyIncome: number
    expenseToIncomeRatio: number
    totalBalance: number
    daysUntilPayday: number
  }
  insights: InsightMessage[]
  warnings: InsightMessage[]
  recommendations: InsightMessage[]
  goals: Array<InsightMessage & {status: string; progress?: number}>
  forecast: {nextMonth: {expenses: number; income: number; balance: number}}
  patterns: {mostActiveDay: {day: string; expenses: number; count: number}}
  summary: {totalTransactions: number; avgTransactionAmount: number; largestCategory: CategoryBreakdown | null}
}
