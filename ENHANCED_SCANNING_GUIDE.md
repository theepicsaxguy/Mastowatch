# Mastowatch Enhanced Scanning System

## Overview

This document describes the comprehensive enhancements made to the Mastowatch scanning system and rules management, addressing the inefficiencies in the original system and adding powerful new features for federated content monitoring and rule management.

## Key Enhancements

### 1. Enhanced Scanning Logic

#### Problem Solved
The original scanning system repeatedly looped over the same rule for a single user, failing to move forward to other accounts or users efficiently.

#### Solution
- **Smart Content Deduplication**: Implemented content hashing to detect when account content hasn't changed
- **Cursor-based Progression**: Enhanced cursor management ensures systematic progression through all accounts
- **Session Tracking**: Scan sessions track progress across multiple users and accounts
- **Cache Management**: Intelligent caching prevents unnecessary re-processing of unchanged content

#### Key Components
- `EnhancedScanningSystem` class in `app/enhanced_scanning.py`
- `ContentScan` model for tracking processed content
- `ScanSession` model for managing scan progress
- Enhanced job tasks with better error handling and progression

### 2. Federated Domain Handling

#### Features
- **Domain Violation Tracking**: Automatic tracking of violations per domain
- **Configurable Thresholds**: Set custom defederation thresholds per domain
- **Automated Defederation**: Automatic marking of domains for defederation when thresholds are exceeded
- **Risk Assessment**: High-risk domains (approaching threshold) are highlighted for manual review

#### Models
- `DomainAlert` model tracks violations and defederation status
- Configurable thresholds with default value of 10 violations
- Automated tracking with manual override capabilities

### 3. Enhanced Rules Management

#### User Interface Improvements
- **Intuitive Rule Creation**: User-friendly interface with examples and descriptions
- **Rule Toggle**: Enable/disable rules without deletion
- **Bulk Operations**: Toggle multiple rules simultaneously
- **Rule Templates**: Example patterns for common use cases

#### Rule Metadata Enhancement
- **Trigger Statistics**: Track how often each rule is triggered
- **Performance Metrics**: Analyze rule effectiveness
- **Historical Data**: Track rule usage over time
- **Content Evidence**: Store content that triggered rules for analysis

#### Database Integration
- Rules stored in database for persistence
- File-based rules (rules.yml) marked as "default" rules
- Seamless integration between file and database rules
- Version tracking for rule changes

### 4. Enhanced Analytics Dashboard

#### New Dashboard Sections

##### Scanning Analytics (`/scanning` tab)
- **Active Sessions**: Real-time view of ongoing scans
- **Session History**: Track completed and failed scans
- **Content Cache Stats**: Monitor scan cache effectiveness
- **Rule Performance**: View most triggered rules and statistics

##### Domain Monitoring (`/domains` tab)
- **Domain Overview**: Summary of monitored, high-risk, and defederated domains
- **Violation Tracking**: Detailed view of violations per domain
- **Risk Assessment**: Visual indicators for domains approaching thresholds
- **Defederation Status**: Track automated and manual defederation decisions

##### Enhanced Rules Tab
- **Rule Statistics**: Performance metrics for each rule
- **Trigger History**: See what content triggered rules
- **Rule Details**: Expanded view with usage analytics
- **Bulk Management**: Multi-select operations for rule management

### 5. Performance Optimizations

#### Caching Strategy
- Content hashing prevents re-scanning unchanged content
- Rule version tracking invalidates cache when rules change
- Configurable cache TTL (default: 24 hours)

#### Database Optimizations
- Strategic indexes for performance
- Efficient pagination with cursor-based navigation
- Optimized queries for analytics endpoints

#### Background Processing
- Async task processing with Celery
- Improved error handling and retry logic
- Better resource management

## New API Endpoints

### Scanning Control
- `POST /scanning/federated` - Trigger federated content scan
- `POST /scanning/domain-check` - Check domain violations
- `POST /scanning/invalidate-cache` - Force cache invalidation

### Enhanced Analytics
- `GET /analytics/scanning` - Scanning progress and statistics
- `GET /analytics/domains` - Domain monitoring data
- `GET /analytics/rules/statistics` - Rule performance metrics

### Rule Management
- `POST /rules/bulk-toggle` - Toggle multiple rules
- `GET /rules/{id}/details` - Detailed rule information
- Enhanced CRUD operations with metadata

## Database Schema Changes

### New Models
```sql
-- Enhanced account tracking
ALTER TABLE accounts ADD COLUMN scan_cursor_position TEXT;
ALTER TABLE accounts ADD COLUMN last_full_scan_at TIMESTAMP;
ALTER TABLE accounts ADD COLUMN content_hash TEXT;

-- Enhanced rule metadata
ALTER TABLE rules ADD COLUMN trigger_count INTEGER DEFAULT 0;
ALTER TABLE rules ADD COLUMN last_triggered_at TIMESTAMP;
ALTER TABLE rules ADD COLUMN last_triggered_content JSON;
ALTER TABLE rules ADD COLUMN created_by TEXT DEFAULT 'system';
ALTER TABLE rules ADD COLUMN updated_by TEXT;
ALTER TABLE rules ADD COLUMN description TEXT;

-- New tables for enhanced functionality
CREATE TABLE domain_alerts (
    id BIGSERIAL PRIMARY KEY,
    domain TEXT UNIQUE NOT NULL,
    violation_count INTEGER DEFAULT 0,
    last_violation_at TIMESTAMP,
    defederation_threshold INTEGER DEFAULT 10,
    is_defederated BOOLEAN DEFAULT FALSE,
    defederated_at TIMESTAMP,
    defederated_by TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE scan_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_type TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    accounts_processed INTEGER DEFAULT 0,
    total_accounts INTEGER,
    current_cursor TEXT,
    last_account_id TEXT,
    rules_applied JSON,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSON
);

CREATE TABLE content_scans (
    id BIGSERIAL PRIMARY KEY,
    content_hash TEXT UNIQUE NOT NULL,
    mastodon_account_id TEXT NOT NULL,
    status_id TEXT,
    scan_type TEXT NOT NULL,
    last_scanned_at TIMESTAMP DEFAULT NOW(),
    scan_result JSON,
    rules_version TEXT,
    needs_rescan BOOLEAN DEFAULT FALSE
);
```

## Configuration Options

### Environment Variables
- `DEFEDERATION_THRESHOLD` - Default threshold for domain defederation (default: 10)
- `CONTENT_CACHE_TTL` - Content cache time-to-live in hours (default: 24)
- `FEDERATED_SCAN_ENABLED` - Enable federated content scanning (default: true)

### Rules Configuration
Enhanced rules.yml with metadata support:
```yaml
report_threshold: 1.0
username_regex:
  - name: "crypto_users"
    pattern: "(ai|gpt|coin|arb|doge)"
    weight: 0.6
    description: "Detects cryptocurrency-related usernames"
display_name_regex:
  - name: "pump_schemes"
    pattern: "pump|airdrops?"
    weight: 0.5
    description: "Identifies pump and dump schemes"
content_regex:
  - name: "giveaway_scams"
    pattern: "giveaway|free\\s+(btc|eth|nft)"
    weight: 0.7
    description: "Catches fake giveaway scams"
```

## Deployment Guide

### Migration Steps
1. **Database Migration**:
   ```bash
   # Run the new migration
   alembic upgrade head
   ```

2. **Environment Setup**:
   ```bash
   # Add new environment variables
   export DEFEDERATION_THRESHOLD=10
   export CONTENT_CACHE_TTL=24
   export FEDERATED_SCAN_ENABLED=true
   ```

3. **Rule Migration**:
   - Existing rules.yml will be automatically imported as "default" rules
   - Custom rules can be added through the UI
   - File-based rules remain read-only, database rules are fully editable

4. **Cache Initialization**:
   ```bash
   # Initialize content scan cache
   curl -X POST /scanning/invalidate-cache
   ```

### Monitoring

#### Health Checks
Enhanced health endpoint now includes:
- Content scan cache status
- Active scan session count
- Domain monitoring status

#### Metrics
New Prometheus metrics:
- `mastowatch_content_scans_total` - Total content scans performed
- `mastowatch_cache_hits_total` - Content cache hit rate
- `mastowatch_domain_violations_total` - Domain violations by domain
- `mastowatch_rule_triggers_total` - Rule trigger count by rule

## Usage Examples

### Starting a Federated Scan
```bash
# Scan all active domains
curl -X POST /scanning/federated

# Scan specific domains
curl -X POST /scanning/federated \
  -H "Content-Type: application/json" \
  -d '{"domains": ["example.com", "test.social"]}'
```

### Managing Rules via API
```bash
# Create a new rule
curl -X POST /rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "spam_keywords",
    "rule_type": "content_regex",
    "pattern": "spam|scam|phishing",
    "weight": 0.8,
    "description": "Detects common spam keywords"
  }'

# Toggle multiple rules
curl -X POST /rules/bulk-toggle \
  -H "Content-Type: application/json" \
  -d '{
    "rule_ids": [1, 2, 3],
    "enabled": false
  }'
```

### Monitoring Domain Violations
```bash
# Get domain analytics
curl /analytics/domains

# Trigger domain violation check
curl -X POST /scanning/domain-check
```

## Best Practices

### Rule Creation
1. **Start with Low Weights**: Begin with weights ≤ 0.5 and adjust based on results
2. **Test Patterns**: Use the dry-run mode to test regex patterns before deployment
3. **Monitor Performance**: Check rule statistics regularly to identify ineffective rules
4. **Document Rules**: Always add descriptions to custom rules

### Scanning Optimization
1. **Cache Management**: Invalidate cache only when necessary to maintain performance
2. **Session Monitoring**: Monitor active scan sessions to prevent overlapping scans
3. **Domain Thresholds**: Set appropriate defederation thresholds based on instance size

### Monitoring
1. **Dashboard Review**: Regular review of all dashboard tabs for system health
2. **Alert Setup**: Configure alerts for high domain violation rates
3. **Performance Tracking**: Monitor scan completion times and cache hit rates

## Troubleshooting

### Common Issues

#### Slow Scanning Performance
- Check content cache hit rate in `/analytics/scanning`
- Consider increasing `CONTENT_CACHE_TTL`
- Monitor database performance with slow query logging

#### High Domain Violations
- Review domain analytics in `/domains` tab
- Adjust `DEFEDERATION_THRESHOLD` if needed
- Manually review high-risk domains

#### Rule Performance Issues
- Check rule statistics in `/analytics/rules/statistics`
- Identify rules with high trigger counts but low effectiveness
- Consider adjusting rule weights or patterns

### Error Recovery
- Scan sessions automatically recover from failures
- Failed scans can be restarted via the dashboard
- Content cache can be invalidated to force fresh scans

## Future Enhancements

### Planned Features
1. **ML-based Rule Suggestions**: Automatic rule generation based on patterns
2. **Federation Network Analysis**: Deeper analysis of federated connections
3. **Advanced Reporting**: Exportable reports and trend analysis
4. **Integration APIs**: Webhooks for external system integration

### Scalability Improvements
1. **Distributed Scanning**: Multi-instance scanning coordination
2. **Cache Clustering**: Redis clustering for large deployments
3. **Database Sharding**: Support for multiple database instances

## Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Review domain analytics and adjust thresholds
2. **Monthly**: Analyze rule performance and optimize patterns
3. **Quarterly**: Review and update defederation policies

### Performance Monitoring
- Monitor dashboard response times
- Track database query performance
- Review scan completion metrics

### Backup and Recovery
- Regular database backups including new tables
- Export rule configurations for disaster recovery
- Monitor scan session state for recovery planning

## Conclusion

These enhancements transform Mastowatch from a basic scanning tool into a comprehensive federated content monitoring and moderation platform. The improved efficiency, enhanced analytics, and powerful rule management capabilities provide administrators with the tools needed to effectively moderate federated content while maintaining system performance.

The modular design ensures that individual components can be enhanced or replaced without affecting the entire system, providing a solid foundation for future development and customization.
