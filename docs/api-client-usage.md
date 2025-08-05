# API Client Usage Guide

## Overview

This project uses a generated OpenAPI client for Mastodon API interactions, ensuring type safety, consistency, and centralized configuration.

## Recommended Usage

### 1. Use the Generated Client

**Preferred:** Always use the generated `Client` or `AuthenticatedClient` from `app.clients.mastodon.client`:

```python
from app.clients.mastodon.client import AuthenticatedClient

# For authenticated endpoints
client = AuthenticatedClient(
    base_url=str(settings.INSTANCE_BASE),
    token=access_token,
    prefix="Bearer",
    timeout=10.0
)

# Use the client's HTTP session for consistency
async with client.get_async_httpx_client() as http_client:
    response = await http_client.get("/api/v1/accounts/verify_credentials")
    data = response.json()
```

### 2. Avoid Direct httpx Usage

**Avoid:** Direct `httpx.Client()` or `httpx.AsyncClient()` instantiation outside `/app/clients/mastodon`:

```python
# ❌ Don't do this
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get(f"{base_url}/api/v1/accounts/verify_credentials")
```

**Instead:** Use the generated client's HTTP session:

```python
# ✅ Do this
from app.clients.mastodon.client import AuthenticatedClient

client = AuthenticatedClient(base_url=base_url, token=token)
async with client.get_async_httpx_client() as http_client:
    response = await http_client.get("/api/v1/accounts/verify_credentials")
```

### 3. High-Level Facade (Optional)

For complex workflows, use `MastoClient` as a high-level facade:

```python
from app.mastodon_client import MastoClient

client = MastoClient(token="your_token")
account = client.get_account("123")
statuses = client.get_account_statuses("123", limit=10)
```

## Benefits of This Approach

1. **Centralized Configuration**: Headers, timeouts, SSL verification, and other settings are managed in one place
2. **Type Safety**: Generated models provide better IDE support and error detection
3. **Consistency**: All HTTP calls use the same transport layer
4. **Rate Limiting**: Centralized rate limiting and metrics collection
5. **Testability**: Easier to mock and test with a consistent interface

## Adding New Endpoints

1. **First choice**: Use the generated client's HTTP session for the new endpoint
2. **If complex**: Add a method to `MastoClient` that uses `_make_raw_request`
3. **Document** any endpoints not in the OpenAPI spec for future addition

## Testing

When testing code that makes API calls:

```python
# Mock the generated client's HTTP session
@patch.object(AuthenticatedClient, 'get_async_httpx_client')
def test_api_call(self, mock_get_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123"}
    
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_get_client.return_value.__aenter__.return_value = mock_client

    # Test your code here
```

## Scanning

`GET /scan/accounts` returns a page of accounts to analyze.

```http
GET /scan/accounts?session_type=remote&limit=50&cursor=12345
```

Response:

```json
{
  "accounts": [{"id": "1"}],
  "next_cursor": "67890"
}
```

Send the `next_cursor` value in the query string to request the following page.
