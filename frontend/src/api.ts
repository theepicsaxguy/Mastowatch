export function getStoredApiKey(): string | null {
  return localStorage.getItem('mw_api_key');
}

export function setStoredApiKey(v: string) {
  localStorage.setItem('mw_api_key', v);
}

type FetchOpts = RequestInit & { apiKey?: string };

export async function apiFetch<T = unknown>(path: string, opts: FetchOpts = {}): Promise<T> {
  const apiKey = opts.apiKey ?? getStoredApiKey() ?? undefined;
  const headers: HeadersInit = {
    'Accept': 'application/json',
    ...(opts.body && !(opts.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
    ...(opts.headers ?? {}),
    ...(apiKey ? { 'X-API-Key': apiKey } : {})
  };
  const res = await fetch(path, { ...opts, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) return res.json() as Promise<T>;
  return (await res.text()) as unknown as T;
}