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
  let retryCount = 0;
  const maxRetries = 3;
  const baseDelay = 1000;
  
  const apiBase = (import.meta as any).env?.VITE_API_URL;
  const isDevelopment = (import.meta as any).env?.DEV;
  const useProxy = isDevelopment && !apiBase?.includes('://');
  
  while (retryCount < maxRetries) {
    try {
      // Use session-based auth only, no Bearer token
      const url = useProxy ? '/api/v1/me' : `${apiBase}/api/v1/me`;
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include' // Include cookies
      });
      
      if (!res.ok) {
        if (res.status === 401) return null;
        throw new Error(`${res.status} ${res.statusText}`);
      }
      
      return await res.json() as User;
    } catch (error: any) {
      if (error.message?.includes('401')) return null;
      if (error.message?.includes('fetch') && retryCount < maxRetries - 1) {
        retryCount++;
        const delay = baseDelay * Math.pow(2, retryCount - 1);
        console.warn(`Failed to connect to API, retrying in ${delay}ms... (${retryCount}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  return null;
}

export async function logout(): Promise<void> {
  // Clear any stored tokens (though we're primarily using session cookies now)
  localStorage.removeItem('auth_token');
  
  const apiBase = (import.meta as any).env?.VITE_API_URL;
  const isDevelopment = (import.meta as any).env?.DEV;
  const useProxy = isDevelopment && !apiBase?.includes('://');
  
  try {
    const url = useProxy ? '/admin/logout' : `${apiBase}/admin/logout`;
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      },
      credentials: 'include' // Include cookies for session-based auth
    });
    
    if (!res.ok) {
      throw new Error(`${res.status} ${res.statusText}`);
    }
  } catch (error) {
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

// Helper function to determine API base URL
function getApiBase(): string {
  const configuredApiBase = (import.meta as any).env?.VITE_API_URL;
  const isDevelopment = (import.meta as any).env?.DEV;
  const useProxy = isDevelopment && !configuredApiBase?.includes('://');
  
  return useProxy ? '' : configuredApiBase;
}

export function redirectToLogin(): void {
  const apiBase = getApiBase();
  window.location.href = `${apiBase}/admin/login`;
}

export function loginWithPopup(): Promise<AuthResponse> {
  return new Promise((resolve, reject) => {
    const apiBase = getApiBase();
    const popup = window.open(
      `${apiBase}/admin/login?popup=true`,
      'oauth-login',
      'width=600,height=700,scrollbars=yes,resizable=yes'
    );
    if (!popup) {
      reject(new Error('Failed to open popup window. Please allow popups for this site.'));
      return;
    }
    const checkClosed = setInterval(() => {
      if (popup.closed) {
        clearInterval(checkClosed);
        reject(new Error('OAuth login was cancelled'));
      }
    }, 1000);
    
    const handleMessage = (event: MessageEvent) => {
      // Only listen to events from the popup
      if (event.source !== popup) return;
      
      if (event.data.type === 'oauth-success') {
        clearInterval(checkClosed);
        popup.close();
        window.removeEventListener('message', handleMessage);
        const authResponse = event.data.auth as AuthResponse;
        
        // Establish session in main window using the access token
        const apiBase = getApiBase();
        const isDevelopment = (import.meta as any).env?.DEV;
        const useProxy = isDevelopment && !apiBase?.includes('://');
        const url = useProxy ? '/admin/establish-session' : `${apiBase}/admin/establish-session`;
        
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // Include cookies
          body: JSON.stringify({ access_token: authResponse.access_token })
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to establish session');
          }
          return response.json();
        })
        .then(() => {
          resolve(authResponse);
        })
        .catch(error => {
          reject(new Error(`Failed to establish session: ${error.message}`));
        });
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
