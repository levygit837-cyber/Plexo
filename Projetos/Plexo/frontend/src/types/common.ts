// Common types used across the application
// Provides base types, utility types, and shared interfaces

export type UUID = string;

export type Timestamp = string;

export type Status = 'active' | 'inactive' | 'pending' | 'error';

export type Priority = 'low' | 'medium' | 'high' | 'critical';

export interface BaseEntity {
  id: UUID;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

export interface PaginationParams {
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginationMeta {
  currentPage: number;
  pageSize: number;
  totalPages: number;
  totalItems: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export interface SelectOption<T = string> {
  label: string;
  value: T;
  disabled?: boolean;
}

export interface ValidationError {
  field: string;
  message: string;
  code?: string;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface User {
  id: UUID;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'viewer' | string;
  createdAt?: Timestamp;
  updatedAt?: Timestamp;
}

export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  status: LoadingState;
}

export type Nullable<T> = T | null;

export type Optional<T> = T | undefined;

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
