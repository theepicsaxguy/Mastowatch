#!/usr/bin/env python3
"""
Migration script to update existing code to use the new type-safe Mastodon client.

This script demonstrates how to migrate from MastoClient to MastoClientV2 with
minimal code changes while gaining type safety benefits.
"""

import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from mastodon_client import MastoClient
from mastodon_client_v2 import MastoClientV2


def compare_clients():
    """Demonstrate the differences between old and new clients."""
    
    # Example token (you'd use a real one)
    token = "fake_token_for_demo"
    
    # Old client
    old_client = MastoClient(token)
    
    # New client
    new_client = MastoClientV2(token)
    
    print("=== Migration Guide ===\n")
    
    print("1. Basic Usage (Backward Compatible)")
    print("   Old: admin.get('/api/v1/admin/accounts', params={'origin': 'remote'})")
    print("   New: admin.get('/api/v1/admin/accounts', params={'origin': 'remote'})")
    print("   → No change required for basic HTTP calls!\n")
    
    print("2. Type-safe Account Fetching")
    print("   Old: r = admin.get(f'/api/v1/accounts/{account_id}')")
    print("        account_data = r.json()")
    print("   New: account = admin.get_account(account_id)")
    print("        # account is now a typed Account object!")
    print("        print(account.username, account.followers_count)\n")
    
    print("3. Type-safe Status Fetching")
    print("   Old: r = admin.get(f'/api/v1/accounts/{account_id}/statuses', params={'limit': 40})")
    print("        statuses = r.json()")
    print("   New: statuses = admin.get_account_statuses(account_id, limit=40)")
    print("        # statuses is now List[Status] with full type info!\n")
    
    print("4. Type-safe Report Creation")
    print("   Old: r = bot.post('/api/v1/reports', data={...})")
    print("        report_id = r.json().get('id')")
    print("   New: report = bot.create_report(account_id, comment, status_ids)")
    print("        report_id = report.id  # Fully typed!\n")
    
    print("5. Admin Endpoints (Unchanged)")
    print("   # Admin endpoints not in OpenAPI spec continue to work as before")
    print("   r = admin.get_admin_accounts(origin='remote', limit=100)")
    print("   accounts = r.json()  # Same as before\n")


def migration_benefits():
    """Show the benefits of migration."""
    
    print("=== Benefits of Migration ===\n")
    
    print("✅ Type Safety")
    print("   - IDE autocomplete for all API responses")
    print("   - Compile-time error checking")
    print("   - Better documentation through types\n")
    
    print("✅ Reduced Errors")
    print("   - No more r.json() typos")
    print("   - Parameter validation")
    print("   - Consistent response handling\n")
    
    print("✅ Backward Compatibility")
    print("   - Legacy .get() and .post() methods still work")
    print("   - Admin endpoints unchanged")
    print("   - Gradual migration possible\n")
    
    print("✅ Better Development Experience")
    print("   - IntelliSense shows available fields")
    print("   - Type hints improve code readability")
    print("   - Easier refactoring\n")


def show_example_migration():
    """Show a real example of migrating existing code."""
    
    print("=== Example: Migrating analyze_and_maybe_report ===\n")
    
    print("BEFORE:")
    print("""
# Old approach - raw HTTP calls
sr = admin.get(f"/api/v1/accounts/{acct_id}/statuses", params={"limit": settings.MAX_STATUSES_TO_FETCH})
statuses = sr.json()  # Could be anything!

# Manual report creation
payload = {"account_id": acct_id, "comment": comment}
for sid in (status_ids or []):
    payload.setdefault("status_ids[]", []).append(sid)
rr = bot.post("/api/v1/reports", data=payload)
rep_id = rr.json().get("id", "")  # Unsafe access
""")
    
    print("AFTER:")
    print("""
# New approach - type-safe calls
statuses = admin.get_account_statuses(acct_id, limit=settings.MAX_STATUSES_TO_FETCH)
# statuses is now List[Status] - fully typed!

# Type-safe report creation
report = bot.create_report(
    account_id=acct_id,
    comment=comment,
    status_ids=status_ids,
    category=settings.REPORT_CATEGORY_DEFAULT,
    forward=is_remote and settings.FORWARD_REMOTE_REPORTS,
    rule_ids=rule_ids if payload["category"] == "violation" else None,
)
rep_id = report.id  # Type-safe access!
""")


if __name__ == "__main__":
    compare_clients()
    migration_benefits()
    show_example_migration()
    
    print("=== Next Steps ===")
    print("1. Import MastoClientV2 in your code")
    print("2. Replace MastoClient instances gradually")
    print("3. Update method calls to use type-safe versions where available")
    print("4. Keep using .get()/.post() for admin endpoints until they're added to OpenAPI spec")
    print("5. Enjoy better IDE support and fewer runtime errors!")
