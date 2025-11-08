import { useQueries } from '@tanstack/react-query'
import { useGetAccounts } from '@entities/account/api/accountApi'
import type { Transaction } from '@entities/transaction'
import type { Account } from '@entities/account'
import { Card, CardContent, Skeleton } from '@shared/ui'
import { formatCurrency } from '@shared/lib/utils'
import { ArrowUpRight, ArrowDownRight, Clock } from 'lucide-react'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import { BANK_NAMES } from '@shared/config'
import { apiClient, ENDPOINTS } from '@shared/api'
import type { TransactionResponse } from '@shared/api/types'

type TransactionWithAccount = Transaction & {
  accountId: string
  account: Account
}

export function TransactionsList() {
  const { data: accounts, isLoading: accountsLoading } = useGetAccounts()

  if (accountsLoading) {
    return (
      <div className="space-y-3">
        <Skeleton className="h-20" />
        <Skeleton className="h-20" />
        <Skeleton className="h-20" />
      </div>
    )
  }

  if (!accounts?.length) {
    return null
  }

  return <TransactionsContent accounts={accounts} />
}

function TransactionsContent({ accounts }: { accounts: Account[] }) {
  const transactionQueries = useQueries({
    queries: accounts.map((account) => ({
      queryKey: ['transactions', account.accountId, account.clientId],
      queryFn: async () => {
        const data = await apiClient.get<TransactionResponse[]>(
          ENDPOINTS.ACCOUNTS.TRANSACTIONS(account.accountId),
          { client_id: account.clientId }
        )
        return data.map((tx) => ({
          id: tx.id,
          date: tx.date,
          description: tx.description,
          amount: tx.amount,
          currency: tx.currency,
          type: tx.type,
        }))
      },
    })),
  })

  const allTransactions: TransactionWithAccount[] = transactionQueries
    .flatMap((query, index) =>
      (query.data || []).map((transaction: Transaction) => ({
        ...transaction,
        account: accounts[index],
      }))
    )
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5)

  if (!allTransactions.length) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Clock className="mb-3 h-12 w-12 text-gray-400" />
            <p className="mb-1 text-sm font-medium text-gray-900">Пока нет транзакций</p>
            <p className="text-xs text-gray-500">
              Транзакции появятся после синхронизации с банками
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-3">
      {allTransactions.map((transaction, index) => (
        <TransactionItem
          key={`dashboard-${transaction.account.accountId}-${transaction.id}-${index}`}
          transaction={transaction}
        />
      ))}
    </div>
  )
}

function TransactionItem({ transaction }: { transaction: TransactionWithAccount }) {
  const isIncome = transaction.amount > 0
  const date = new Date(transaction.date)
  const bankName =
    BANK_NAMES[transaction.account.clientId as keyof typeof BANK_NAMES] ||
    transaction.account.clientName

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className={`flex h-10 w-10 items-center justify-center rounded-full ${
                isIncome ? 'bg-green-100' : 'bg-red-100'
              }`}
            >
              {isIncome ? (
                <ArrowDownRight className="h-5 w-5 text-green-600" />
              ) : (
                <ArrowUpRight className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div>
              <p className="font-medium text-gray-900">{transaction.description}</p>
              <p className="text-xs text-gray-500">
                {format(date, 'd MMMM yyyy, HH:mm', { locale: ru })}
              </p>
              <p className="text-xs text-gray-500">
                {transaction.account.accountName} • {bankName}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className={`text-lg font-semibold ${isIncome ? 'text-green-600' : 'text-red-600'}`}>
              {isIncome && '+'}
              {formatCurrency(Math.abs(transaction.amount), transaction.currency)}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
