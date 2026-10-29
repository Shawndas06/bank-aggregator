import { strict as assert } from 'node:assert'
import { test } from 'node:test'
import { bankTransaction, paymentTransaction } from '../src/entities/transaction/model/aggregate.ts'
import { mapUserResponse } from '../src/entities/user/model/mapUser.ts'
import { mapLoyaltyCard, serializeLoyaltyCard } from '../src/entities/account/model/loyalty-card.ts'
import { asError } from '../src/shared/lib/errors.ts'
import type { Account } from '../src/entities/account/model/types.ts'
import type { PaymentResponse } from '../src/shared/api/types.ts'

const accounts: Account[] = [
  {
    id: 1,
    accountId: 'bank-a',
    accountName: 'First',
    clientId: 1,
    clientName: 'VBank',
    isActive: true,
  },
  {
    id: 2,
    accountId: 'bank-b',
    accountName: 'Second',
    clientId: 2,
    clientName: 'SBank',
    isActive: true,
  },
]
const payment: PaymentResponse = {
  id: 4,
  amount: 0.25,
  currency: 'RUB',
  paymentType: 'to_person',
  status: 'completed',
  isIncoming: false,
  createdAt: '2030-01-01T12:00:00',
  completedAt: '2030-01-01T12:00:05',
  fromAccountName: 'Second',
  toName: 'Recipient',
}

test('bank transaction retains its source account and identity', () => {
  const result = bankTransaction(
    {
      id: 'bank-tx',
      amount: -0.25,
      currency: 'RUB',
      type: 'debit',
      date: payment.createdAt,
      description: 'Shop',
    },
    accounts[1]
  )
  assert.equal(result.accountId, 'bank-b')
  assert.equal(result.account.id, 2)
  assert.equal(result.amount, -0.25)
  assert.equal(result.id, 'bank-tx')
})
for (const incoming of [true, false]) {
  for (const amount of [0, 0.25, 100, -100]) {
    test(`payment sign/account survives mapping: incoming=${incoming}, amount=${amount}`, () => {
      const result = paymentTransaction({ ...payment, amount, isIncoming: incoming }, accounts)!
      assert.equal(result.amount, incoming ? Math.abs(amount) : -Math.abs(amount))
      assert.equal(result.type, incoming ? 'credit' : 'debit')
      assert.equal(result.accountId, incoming ? 'bank-a' : 'bank-b')
      assert.equal(result.date, payment.completedAt)
      assert.equal(result.id, 'payment_4')
    })
  }
}
test('payment mapping handles missing accounts, completion and description', () => {
  assert.equal(paymentTransaction(payment, []), null)
  const result = paymentTransaction(
    { ...payment, completedAt: null, paymentType: 'premium' },
    accounts
  )!
  assert.equal(result.date, payment.createdAt)
  assert.equal(result.description, 'Оплата Premium подписки')
  assert.equal(
    paymentTransaction({ ...payment, description: 'Keep' }, accounts)!.description,
    'Keep'
  )
})
for (const phone of [null, '+79000000001']) {
  for (const accountType of ['free', 'premium'] as const) {
    test(`profile retains wire fields: ${accountType}, ${phone}`, () => {
      const source = {
        id: 1,
        name: 'Test',
        birthDate: '1990-01-01',
        email: 'user@example.test',
        phone,
        accountType,
        avatarUrl: null,
        isVerified: true,
      }
      assert.deepEqual(mapUserResponse(source), source)
    })
  }
}
test('loyalty list and create use the real snake_case API contract', () => {
  const result = mapLoyaltyCard({
    id: 1,
    card_type: 'magnit',
    card_name: 'Test',
    masked_number: '****1234',
    barcode_type: 'EAN13',
    created_at: payment.createdAt,
  })
  assert.equal(result.cardType, 'MAGNIT')
  assert.equal(result.maskedNumber, '****1234')
  const request = serializeLoyaltyCard({
    cardType: 'MAGNIT',
    cardNumber: '1234567890123',
    barcodeType: 'EAN13',
    cardName: 'Test',
  })
  assert.deepEqual(request, {
    card_type: 'magnit',
    card_number: '1234567890123',
    barcode_type: 'EAN13',
    card_name: 'Test',
  })
})
test('unknown thrown values are usable without unsafe assertions', () => {
  const original = new Error('test')
  assert.equal(asError(original), original)
  assert.equal(asError('camera denied').message, 'camera denied')
  assert.equal(asError(null).message, 'null')
})
