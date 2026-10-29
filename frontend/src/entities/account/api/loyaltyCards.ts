import { apiClient } from '@shared/api'
import type { LoyaltyCardCreate } from '@shared/api/types'
import { mapLoyaltyCard, serializeLoyaltyCard, type CardResponse } from '../model/loyalty-card'

export async function getLoyaltyCards() {
  const data = await apiClient.get<CardResponse[]>('/api/loyalty-cards')
  return data.map(mapLoyaltyCard)
}

export function createLoyaltyCard(card: LoyaltyCardCreate) {
  return apiClient.post('/api/loyalty-cards', serializeLoyaltyCard(card))
}
