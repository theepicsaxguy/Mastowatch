#!/usr/bin/env python3
"""
Test script to demonstrate the type-safe Mastodon client functionality.
This shows the benefits of the new OpenAPI-based client vs the legacy one.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

try:
    from mastodon_client_v2 import MastoClient
    from clients.mastodon.models import Account, Status
    print("✅ Successfully imported type-safe client")
except ImportError as e:
    print(f"❌ Failed to import type-safe client: {e}")
    print("Make sure you've generated the client with: make regenerate-client")
    sys.exit(1)

def test_type_annotations():
    """Test that type annotations are working correctly."""
    print("\n🔍 Testing type annotations...")
    
    # This would be a real client in production
    # client = MastoClient("fake_token_for_testing")
    
    # Check that we can import all the expected types
    from clients.mastodon.models.account import Account
    from clients.mastodon.models.status import Status
    from clients.mastodon.models.report import Report
    from clients.mastodon.models.create_report_body import CreateReportBody
    
    print("✅ All type imports successful")
    
    # Show available methods
    methods = [m for m in dir(MastoClient) if not m.startswith('_')]
    print(f"✅ MastoClient has {len(methods)} public methods")
    
    # Check for type-safe methods
    type_safe_methods = [
        'get_account', 'get_account_statuses', 'create_report'
    ]
    
    for method in type_safe_methods:
        if hasattr(MastoClient, method):
            print(f"✅ Type-safe method available: {method}")
        else:
            print(f"❌ Type-safe method missing: {method}")
    
    # Check for legacy compatibility
    legacy_methods = ['get', 'post', 'get_admin_accounts']
    for method in legacy_methods:
        if hasattr(MastoClient, method):
            print(f"✅ Legacy compatibility method: {method}")
        else:
            print(f"❌ Legacy compatibility missing: {method}")

def show_api_coverage():
    """Show what API endpoints are available in the generated client."""
    print("\n📊 API Coverage Analysis...")
    
    from pathlib import Path
    api_dir = Path(__file__).parent.parent / "app" / "clients" / "mastodon" / "api"
    
    if not api_dir.exists():
        print("❌ Generated API client not found")
        return
    
    # Count endpoints by category
    categories = {}
    total_endpoints = 0
    
    for category_dir in api_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith('__'):
            endpoints = list(category_dir.glob("*.py"))
            endpoints = [e for e in endpoints if not e.name.startswith('__')]
            categories[category_dir.name] = len(endpoints)
            total_endpoints += len(endpoints)
    
    print(f"📈 Total API endpoints: {total_endpoints}")
    print("📋 Endpoints by category:")
    
    for category, count in sorted(categories.items()):
        print(f"   {category:20} {count:3d} endpoints")
    
    # Check for admin endpoints
    admin_endpoints = [cat for cat in categories.keys() if 'admin' in cat.lower()]
    if admin_endpoints:
        print(f"⚠️  Admin endpoints found: {admin_endpoints}")
        print("   Note: Admin endpoints in community spec may be limited")
    else:
        print("ℹ️  No admin endpoints in generated client (expected)")
        print("   Admin operations use fallback HTTP methods")

def main():
    """Run all tests and show status."""
    print("🧪 Testing Mastodon API Client Integration")
    print("=" * 50)
    
    test_type_annotations()
    show_api_coverage()
    
    print("\n✅ Type-safe Mastodon client is ready!")
    print("\n🚀 Next steps:")
    print("   1. Update your code to use MastoClient")
    print("   2. Enjoy type safety and better IDE support")
    print("   3. Use fallback methods for admin endpoints")
    print("   4. Run 'make update-mastodon-client' periodically for updates")
    
    print(f"\n📚 Documentation: {Path(__file__).parent.parent}/docs/mastodon-api-client.md")

if __name__ == "__main__":
    main()
