import { apiFetch } from './api';

export interface User {
  id: string;
  username: string;
  acct: string;
  display_name: string;
  is_admin: boolean;
  avatar?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
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
  // Clear stored token
  localStorage.removeItem('auth_token');
  
  // Call logout endpoint (will clear cookies if any)
  try {
    await apiFetch('/admin/logout', {
      method: 'POST'
    });
  } catch (error) {
    // Ignore errors on logout
    console.warn('Logout endpoint failed:', error);
  }
}

export function getStoredToken(): string | null {
  return localStorage.getItem('auth_token');
}

export function setStoredToken(token: string): void {
  localStorage.setItem('auth_token', token);
}

export function clearStoredToken(): void {
  localStorage.removeItem('auth_token');
}

// Get API base URL from environment or default
const apiBase = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8080';

export function redirectToLogin(): void {
  // Redirect directly to the API server for OAuth login
  window.location.href = `${apiBase}/admin/login`;
}

/**
 * Start OAuth flow in a popup window and get token
 * This is the preferred method as it doesn't require redirects
 */
export function loginWithPopup(): Promise<AuthResponse> {
  return new Promise((resolve, reject) => {
    // Create popup for OAuth flow with popup parameter
    const popup = window.open(
      `${apiBase}/admin/login?popup=true`,
      'oauth-login',
      'width=600,height=700,scrollbars=yes,resizable=yes'
    );

    if (!popup) {
      reject(new Error('Failed to open popup window. Please allow popups for this site.'));
      return;
    }

    // Poll for completion
    const checkClosed = setInterval(() => {
      if (popup.closed) {
        clearInterval(checkClosed);
        reject(new Error('OAuth login was cancelled'));
      }
    }, 1000);

    // Listen for messages from the popup
    const handleMessage = (event: MessageEvent) => {
      // Verify origin for security
      if (event.origin !== apiBase) {
        return;
      }

      if (event.data.type === 'oauth-success') {
        clearInterval(checkClosed);
        popup.close();
        window.removeEventListener('message', handleMessage);
        
        const authResponse = event.data.auth as AuthResponse;
        setStoredToken(authResponse.access_token);
        resolve(authResponse);
      } else if (event.data.type === 'oauth-error') {
        clearInterval(checkClosed);
        popup.close();
        window.removeEventListener('message', handleMessage);
        reject(new Error(event.data.error || 'OAuth login failed'));
      }
    };

    window.addEventListener('message', handleMessage);
  });
}

/**
 * Attempt token-based login first, fallback to redirect
 */
export async function login(): Promise<User | null> {
  try {
    const authResponse = await loginWithPopup();
    return authResponse.user;
  } catch (error) {
    console.warn('Popup login failed, falling back to redirect:', error);
    redirectToLogin();
    return null;
  }
}
