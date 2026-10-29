import type { UserResponse } from '../../../shared/api/types'
import type { User } from './types'
export function mapUserResponse(response: UserResponse): User {
  return {
    id: response.id,
    email: response.email,
    phone: response.phone,
    avatarUrl: response.avatarUrl,
    isVerified: response.isVerified,
    name: response.name,
    birthDate: response.birthDate,
    accountType: response.accountType,
  }
}
