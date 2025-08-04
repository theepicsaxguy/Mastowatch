const apiBase = (import.meta as any).env?.VITE_API_URL;

export function getStoredApiKey(): string | null {
  return localStorage.getItem('mw_api_key');
}

export function setStoredApiKey(v: string) {
  localStorage.setItem('mw_api_key', v);
}

export function getStoredAuthToken(): string | null {
  return localStorage.getItem('auth_token');
}

type FetchOpts = RequestInit & { apiKey?: string };

export async function apiFetch<T = unknown>(path: string, opts: FetchOpts = {}): Promise<T> {
  const apiKey = opts.apiKey ?? getStoredApiKey() ?? undefined;
  const authToken = getStoredAuthToken();
  
  const url = path.startsWith('http') ? path : apiBase + path;
  
  const headers: HeadersInit = {
    'Accept': 'application/json',
    ...(opts.body && !(opts.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
    ...(opts.headers ?? {}),
    ...(apiKey ? { 'X-API-Key': apiKey } : {}),
    ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {})
  };
  
  const res = await fetch(url, { ...opts, headers });
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