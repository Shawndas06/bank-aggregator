import type { ApiResponse } from './types'

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: unknown
  params?: Record<string, string | number | boolean | undefined>
}

async function request<T>(url: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, params } = options

  // Build URL with query params
  let finalUrl = url
  if (params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, String(value))
      }
    })
    const queryString = searchParams.toString()
    if (queryString) {
      finalUrl = `${url}?${queryString}`
    }
  }

  try {
    const response = await fetch(finalUrl, {
      method,
      credentials: 'include', // Important for cookies
      headers: {
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    })

    // Parse response
    const data: ApiResponse<T> = await response.json()

    // Handle API errors
    if (!data.success) {
      throw new ApiError(data.error.message, response.status, data.error.details)
    }

    return data.data
  } catch (error) {
    // Network errors or JSON parsing errors
    if (error instanceof ApiError) {
      throw error
    }

    throw new ApiError(error instanceof Error ? error.message : 'Network error', undefined, error)
  }
}

export const apiClient = {
  get: <T>(url: string, params?: Record<string, string | number | boolean | undefined>) =>
    request<T>(url, { method: 'GET', params }),

  post: <T>(url: string, body?: unknown) => request<T>(url, { method: 'POST', body }),

  put: <T>(url: string, body?: unknown) => request<T>(url, { method: 'PUT', body }),

  delete: <T>(url: string, body?: unknown) => request<T>(url, { method: 'DELETE', body }),
}

export { ApiError }
