import type { LoyaltyCard, LoyaltyCardCreate } from '../../../shared/api/types'
export type CardResponse = {
  id: number
  card_type: string
  card_name: string
  masked_number: string
  barcode_type: string
  created_at: string
}

export function mapLoyaltyCard(card: CardResponse): LoyaltyCard {
  return {
    id: card.id,
    cardType: card.card_type.toUpperCase(),
    cardName: card.card_name,
    maskedNumber: card.masked_number,
    barcodeType: card.barcode_type,
    createdAt: card.created_at,
  }
}

export function serializeLoyaltyCard(card: LoyaltyCardCreate) {
  return {
    card_type: card.cardType.toLowerCase(),
    card_number: card.cardNumber,
    card_name: card.cardName,
    barcode_type: card.barcodeType,
  }
}
