# Mastodon API Client Integration

This document explains how Mastowatch uses a type-safe, automatically-updated Mastodon API client.

## Overview

We use the [abraham/mastodon-openapi](https://github.com/abraham/mastodon-openapi) project as a Git submodule to:

1. **Track API changes** - The upstream repository is automatically updated weekly with the latest Mastodon API
2. **Generate type-safe clients** - We generate Python clients from the OpenAPI spec for better development experience
3. **Maintain reproducibility** - Git submodules ensure everyone uses the exact same API specification version

## Architecture

```
Mastowatch/
├── specs/
│   ├── mastodon-openapi/           # Git submodule tracking abraham/mastodon-openapi
│   │   └── dist/schema.json        # Pre-built OpenAPI specification
│   └── openapi.json               # Our copy of the spec
├── app/
│   ├── clients/mastodon/          # Generated Python client
│   └── mastodon_client.py         # Type-safe client with admin fallbacks
└── scripts/
    └── update_mastodon_client.sh  # Management script
```

## Mastodon Client

### MastoClient
- **Type-safe** methods for common endpoints (accounts, statuses, reports)
- **Fallback** to raw HTTP for admin endpoints not in OpenAPI spec
- **Full compatibility** with existing rate limiting and metrics
- **Auto-completion** and validation in IDEs

## Usage Examples

### Type-safe Account Operations
```python
from app.mastodon_client_v2 import MastoClient

client = MastoClient(token)

# Get account with full type safety
account = client.get_account("123456")
print(f"@{account.username} has {account.followers_count} followers")

# Get statuses with typed responses
statuses = client.get_account_statuses(
    account_id="123456",
    limit=50,
    exclude_reblogs=True
)
for status in statuses:
    print(f"Status {status.id}: {len(status.content)} characters")
```

### Type-safe Report Creation
```python
# Create a report with full validation
report = client.create_report(
    account_id="123456",
    comment="Automated report based on rule violations",
    status_ids=["789", "101112"],
    category="violation",
    forward=True,
    rule_ids=["rule_1", "rule_2"]
)
print(f"Report created with ID: {report.id}")
```

### Admin Operations (Fallback)
```python
# Admin endpoints not in OpenAPI spec use raw HTTP
response = client.get_admin_accounts(origin="remote", limit=100)
accounts = response.json()
```

## Management Commands

### Script Commands
```bash
# Show current status
./scripts/update_mastodon_client.sh status

# Update submodule and copy latest schema
./scripts/update_mastodon_client.sh update-schema

# Regenerate Python client from current schema
./scripts/update_mastodon_client.sh regenerate

# Full update: submodule + schema + client
./scripts/update_mastodon_client.sh update
```

### Makefile Targets
```bash
# Show API client status
make api-client-status

# Update schema from submodule
make update-api-spec

# Regenerate client
make regenerate-client

# Full update
make update-mastodon-client
```

## Client Usage

### Basic Usage

```python
from app.mastodon_client import MastoClient

# Initialize client
admin = MastoClient(settings.ADMIN_TOKEN)
bot = MastoClient(settings.BOT_TOKEN)
```

### Type-safe Operations

```python
# Get account with full type safety
account = admin.get_account(account_id)
# account.username, account.followers_count, etc. are all typed!

# Get account statuses
statuses = admin.get_account_statuses(account_id, limit=40)
# statuses is List[Status] with full type information

# Create reports
report = bot.create_report(
    account_id=account_id,
    comment="Automated moderation report",
    status_ids=status_ids
)
# report.id is typed and available
```

### Admin Endpoints (Raw HTTP)

```python
# Admin endpoints not in OpenAPI spec use raw HTTP
response = admin.get("/api/v1/admin/accounts", params={"origin": "remote"})
accounts = response.json()
```

### Benefits

- ✅ **Type Safety**: IDE autocomplete and compile-time validation
- ✅ **Fewer Errors**: No more `.json()` typos or missing fields
- ✅ **Better Documentation**: Types serve as documentation
- ✅ **Easier Refactoring**: Type-aware code transformations
- ✅ **Backward Compatibility**: Raw HTTP methods for missing endpoints

## Automation

### Submodule Updates

The abraham/mastodon-openapi repository is automatically updated weekly via GitHub Actions. To get these updates:

1. **Manual update:**
   ```bash
   make update-api-spec
   ```

2. **CI/CD automation** (see `.github/workflows/` for examples)

### Version Tracking

- **Submodule commit** tracks exact API specification version
- **Generated client** reflects the capabilities at generation time
- **Schema backup** created automatically before updates

## Troubleshooting

### Common Issues

1. **Missing admin endpoints:**
   - Admin endpoints may not be in the community OpenAPI spec
   - Use legacy `.get()` and `.post()` methods for these
   - Contribute missing endpoints to abraham/mastodon-openapi

2. **Generation warnings:**
   - Some endpoints may have parsing issues in the generator
   - Check `/tmp/openapi-generate.log` for details
   - Usually safe to ignore, client still works

3. **Submodule issues:**
   ```bash
   # Re-initialize submodule
   git submodule update --init --recursive
   
   # Force update to latest
   git submodule update --remote --force
   ```

### Debugging

1. **Check status:**
   ```bash
   make api-client-status
   ```

2. **Verbose generation:**
   ```bash
   openapi-python-client generate --path specs/openapi.json --meta none --verbose
   ```

3. **Validate schema:**
   ```bash
   python -m json.tool specs/openapi.json > /dev/null
   ```

## Contributing

### Adding New Endpoints

1. **Check if endpoint exists** in generated client
2. **Add to MastoClient** if available in OpenAPI spec
3. **Use fallback method** if admin-only or missing from spec
4. **Consider contributing** missing endpoints to abraham/mastodon-openapi

### Schema Updates

1. **Test with latest schema:**
   ```bash
   make update-mastodon-client
   python -m pytest tests/
   ```

2. **Update type annotations** if API changes
3. **Add backward compatibility** for breaking changes
4. **Document migration steps** for major changes

## Future Improvements

- [ ] Complete admin endpoint coverage in community OpenAPI spec
- [ ] Automated weekly submodule updates via CI/CD
- [ ] Integration testing against live Mastodon instances
- [ ] Performance benchmarking vs legacy client
- [ ] Generated client caching and optimization
