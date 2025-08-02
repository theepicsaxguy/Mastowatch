import { apiFetch } from './api';

export interface User {
  id: string;
  username: string;
  acct: string;
  display_name: string;
  is_admin: boolean;
  avatar?: string;
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const response = await apiFetch<User>('/api/v1/me');
    return response;
  } catch (error: any) {
    if (error.status === 401) {
      return null; // Not authenticated
    }
    throw error;
  }
}

export async function logout(): Promise<void> {
  await apiFetch('/admin/logout', {
    method: 'POST'
  });
}

export function redirectToLogin(): void {
  window.location.href = '/admin/login';
}
