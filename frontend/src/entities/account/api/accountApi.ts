import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient, ENDPOINTS } from '@shared/api'
import type {
  AccountResponse,
  BalanceResponse,
  TransactionResponse,
  AccountCreateRequest,
} from '@shared/api/types'
import type { Account, Balance, Transaction } from '../model/types'

function mapAccount(response: AccountResponse): Account {
  return {
    accountId: response.accountId,
    clientId: response.clientId,
    clientName: response.clientName,
    accountName: response.accountName,
    isActive: response.isActive,
  }
}

function mapBalance(response: BalanceResponse): Balance {
  return {
    amount: response.amount,
    currency: response.currency,
  }
}

function mapTransaction(response: TransactionResponse): Transaction {
  return {
    id: response.id,
    date: response.date,
    description: response.description,
    amount: response.amount,
    currency: response.currency,
    type: response.type,
  }
}

export function useGetAccounts(clientId?: number) {
  return useQuery({
    queryKey: ['accounts', clientId],
    queryFn: async () => {
      const data = await apiClient.get<AccountResponse[]>(
        ENDPOINTS.ACCOUNTS.LIST,
        clientId ? { client_id: clientId } : undefined
      )
      return data.map(mapAccount)
    },
  })
}

export function useGetBalance(accountId: string, clientId?: number) {
  return useQuery({
    queryKey: ['balance', accountId, clientId],
    queryFn: async () => {
      const params: Record<string, string | number> = {}

      if (clientId) {
        params.client_id = clientId
      }

      const data = await apiClient.get<BalanceResponse>(
        ENDPOINTS.ACCOUNTS.BALANCES(accountId),
        params
      )
      return mapBalance(data)
    },
    enabled: !!accountId && !!clientId,
  })
}

export type TransactionsParams = {
  clientId?: number
  offset?: number
  limit?: number
  startDate?: string
  endDate?: string
}

export function useGetTransactions(accountId: string, params?: TransactionsParams) {
  return useQuery({
    queryKey: ['transactions', accountId, params],
    queryFn: async () => {
      const queryParams: Record<string, string | number> = {}

      if (params?.clientId) {
        queryParams.client_id = params.clientId
      }

      if (params?.offset !== undefined) {
        queryParams.offset = params.offset
      }

      if (params?.limit !== undefined) {
        queryParams.limit = params.limit
      }

      if (params?.startDate) {
        queryParams.start_date = params.startDate
      }

      if (params?.endDate) {
        queryParams.end_date = params.endDate
      }

      const data = await apiClient.get<TransactionResponse[]>(
        ENDPOINTS.ACCOUNTS.TRANSACTIONS(accountId),
        queryParams
      )
      return data.map(mapTransaction)
    },
    enabled: !!accountId && !!params?.clientId,
  })
}

export function useCreateAccount() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (request: AccountCreateRequest) =>
      apiClient.post(ENDPOINTS.ACCOUNTS.CREATE, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] })
    },
  })
}
