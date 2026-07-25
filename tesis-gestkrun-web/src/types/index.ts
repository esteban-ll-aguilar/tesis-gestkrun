export * from './domain/auth'
export * from './domain/project'
export * from './domain/backlog'
export * from './domain/sprint'
export * from './domain/task'
export * from './domain/board'
export * from './domain/chat'
export * from './domain/artifact'

export interface PaginatedResponse<T> {
  data: T[]
  nextCursor: string | null
  hasMore: boolean
}

export interface ApiError {
  type: string
  title: string
  status: number
  detail: string
  errors?: Record<string, string[]>
}
