import { apiClient, ENDPOINTS } from '@shared/api'
import type { UserResponse } from '@shared/api/types'
import { useQuery } from '@tanstack/react-query'
import { mapUserResponse } from '../model/mapUser'

export function useGetMe() {
  return useQuery({
    queryKey: ['user', 'me'],
    queryFn: async () => {
      const data = await apiClient.get<UserResponse>(ENDPOINTS.AUTH.ME)
      return mapUserResponse(data)
    },
    retry: false,
  })
}
