import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@shared/api'
import type {
  Obligation, Contribution, SharedResource, Forecast,
  ObligationCreateRequest, ContributionCreateRequest, SharedResourceCreateRequest,
} from '../model/types'

const base = (groupId: number) => `/api/family-plan/${groupId}`

// ─── Обязательства ────────────────────────────────────────────────────────────

export function useObligations(groupId: number, includePaid = false) {
  return useQuery({
    queryKey: ['obligations', groupId, includePaid],
    queryFn: () =>
      apiClient.get<Obligation[]>(`${base(groupId)}/obligations`, {
        include_paid: includePaid,
      }),
    enabled: !!groupId,
  })
}

export function useCreateObligation(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: ObligationCreateRequest) =>
      apiClient.post<Obligation>(`${base(groupId)}/obligations`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['obligations', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

export function useMarkObligationPaid(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (obligationId: number) =>
      apiClient.post(`${base(groupId)}/obligations/${obligationId}/pay`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['obligations', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

export function useDeleteObligation(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (obligationId: number) =>
      apiClient.delete(`${base(groupId)}/obligations/${obligationId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['obligations', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

// ─── Взносы ───────────────────────────────────────────────────────────────────

export function useContributions(groupId: number) {
  return useQuery({
    queryKey: ['contributions', groupId],
    queryFn: () => apiClient.get<Contribution[]>(`${base(groupId)}/contributions`),
    enabled: !!groupId,
  })
}

export function useCreateContribution(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: ContributionCreateRequest) =>
      apiClient.post<Contribution>(`${base(groupId)}/contributions`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['contributions', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

export function useConfirmContribution(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (contributionId: number) =>
      apiClient.post(`${base(groupId)}/contributions/${contributionId}/confirm`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['contributions', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

export function useCancelContribution(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (contributionId: number) =>
      apiClient.post(`${base(groupId)}/contributions/${contributionId}/cancel`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['contributions', groupId] })
      qc.invalidateQueries({ queryKey: ['forecast', groupId] })
    },
  })
}

// ─── Общие ресурсы ────────────────────────────────────────────────────────────

export function useSharedResources(groupId: number) {
  return useQuery({
    queryKey: ['shared-resources', groupId],
    queryFn: () => apiClient.get<SharedResource[]>(`${base(groupId)}/resources`),
    enabled: !!groupId,
  })
}

export function useSetSharedResource(groupId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: SharedResourceCreateRequest) =>
      apiClient.post<SharedResource>(`${base(groupId)}/resources`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['shared-resources', groupId] })
    },
  })
}

// ─── Прогноз ──────────────────────────────────────────────────────────────────

export function useForecast(
  groupId: number,
  includedBalanceRub: number,
  reserveRub = 5000,
  daysAhead = 30,
) {
  return useQuery({
    queryKey: ['forecast', groupId, includedBalanceRub, reserveRub, daysAhead],
    queryFn: () =>
      apiClient.get<Forecast>(`${base(groupId)}/forecast`, {
        included_balance_rub: includedBalanceRub,
        reserve_rub: reserveRub,
        days_ahead: daysAhead,
      }),
    enabled: !!groupId && includedBalanceRub >= 0,
  })
}
