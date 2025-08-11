const apiBase = (import.meta as any).env?.VITE_API_URL;

// In development with Vite proxy, use relative URLs to stay on same origin
const isDevelopment = import.meta.env.DEV;
const useProxy = isDevelopment && !apiBase?.includes('://');

export function getStoredApiKey(): string | null {
  return localStorage.getItem('mw_api_key');
}

export function setStoredApiKey(v: string) {
  localStorage.setItem('mw_api_key', v);
}

type FetchOpts = RequestInit & { apiKey?: string };

export async function apiFetch<T = unknown>(path: string, opts: FetchOpts = {}): Promise<T> {
  const apiKey = opts.apiKey ?? getStoredApiKey() ?? undefined;
  
  // Use relative URLs in development to leverage Vite proxy, absolute URLs otherwise
  const url = path.startsWith('http') ? path : 
              (useProxy ? path : apiBase + path);
  
  const headers: HeadersInit = {
    'Accept': 'application/json',
    ...(opts.body && !(opts.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
    ...(opts.headers ?? {}),
    ...(apiKey ? { 'X-API-Key': apiKey } : {})
  };
  
  const res = await fetch(url, { 
    ...opts, 
    headers,
    credentials: 'include' // Include cookies for session-based authentication
  });
  if (!res.ok) {
    const text = await res.text();
    const error = new Error(`${res.status} ${res.statusText}: ${text}`) as any;
    error.status = res.status;
    throw error;
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) return res.json() as Promise<T>;
  return (await res.text()) as unknown as T;
}