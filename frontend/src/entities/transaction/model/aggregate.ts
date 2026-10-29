import type { PaymentResponse, TransactionResponse } from '../../../shared/api/types'
import type { Account } from '../../account/model/types'
import type { Transaction } from './types'

export type TransactionWithAccount = Transaction & {
  account: Account
  paymentDetails?: PaymentResponse
}

export function bankTransaction(
  transaction: TransactionResponse,
  account: Account
): TransactionWithAccount {
  return { ...transaction, accountId: account.accountId, account }
}

export function paymentTransaction(
  payment: PaymentResponse,
  accounts: Account[]
): TransactionWithAccount | null {
  const account = payment.isIncoming
    ? accounts[0]
    : accounts.find((a) => a.accountName === payment.fromAccountName) || accounts[0]
  if (!account) return null
  let description = payment.description
  if (!description) {
    if (payment.paymentType === 'to_person') {
      description = payment.isIncoming
        ? `Перевод от ${payment.fromUserId ? 'пользователя' : payment.fromAccountName || ''}`
        : `Перевод ${payment.toName || payment.toPhone || ''}`
    } else if (payment.paymentType === 'premium') description = 'Оплата Premium подписки'
    else description = 'Платеж'
  }
  return {
    id: `payment_${payment.id}`,
    accountId: account.accountId,
    account,
    date: payment.completedAt || payment.createdAt,
    description,
    amount: payment.isIncoming ? Math.abs(payment.amount) : -Math.abs(payment.amount),
    currency: payment.currency || 'RUB',
    type: payment.isIncoming ? 'credit' : 'debit',
    paymentDetails: payment,
  }
}
