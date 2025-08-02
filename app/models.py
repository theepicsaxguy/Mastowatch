from sqlalchemy import JSON, TIMESTAMP, BigInteger, Boolean, Column, Numeric, Text, Integer, ForeignKey, Enum as sa_Enum
from sqlalchemy.sql import func

from app.db import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(BigInteger, primary_key=True)
    mastodon_account_id = Column(Text, unique=True, nullable=False)
    acct = Column(Text, nullable=False)
    domain = Column(Text, nullable=False)
    last_checked_at = Column(TIMESTAMP(timezone=True))
    last_status_seen_id = Column(Text)
    # Enhanced fields for better scanning management
    scan_cursor_position = Column(Text)  # Tracks position in status scanning
    last_full_scan_at = Column(TIMESTAMP(timezone=True))  # When we last did a complete scan
    content_hash = Column(Text)  # Hash of account metadata to detect changes


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(BigInteger, primary_key=True)
    mastodon_account_id = Column(Text, nullable=False)
    status_id = Column(Text)
    rule_key = Column(Text, nullable=False)
    score = Column(Numeric, nullable=False)
    evidence = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Report(Base):
    __tablename__ = "reports"
    id = Column(BigInteger, primary_key=True)
    mastodon_account_id = Column(Text, nullable=False)
    status_id = Column(Text)
    mastodon_report_id = Column(Text)
    dedupe_key = Column(Text, unique=True, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Config(Base):
    __tablename__ = "config"
    key = Column(Text, primary_key=True)
    value = Column(JSON, nullable=False)
    updated_by = Column(Text)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Cursor(Base):
    __tablename__ = "cursors"
    name = Column(Text, primary_key=True)
    position = Column(Text, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Rule(Base):
    __tablename__ = "rules"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    # Change rule_type to detector_type
    detector_type = Column(Text, nullable=False)  # e.g., 'regex', 'keyword', 'behavioral'
    pattern = Column(Text, nullable=False)
    weight = Column(Numeric, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    is_default = Column(Boolean, nullable=False, default=False)  # True for rules from rules.yml
    # New columns for action types and duration
    action_type = Column(sa_Enum('report', 'silence', 'suspend', 'disable', 'sensitive', 'domain_block', name='action_type_enum', create_type=False), nullable=False)
    action_duration_seconds = Column(Integer, nullable=True)
    action_warning_text = Column(Text, nullable=True)
    warning_preset_id = Column(Text, nullable=True)
    trigger_threshold = Column(Numeric, nullable=False, default=1.0)
    # Enhanced metadata fields
    trigger_count = Column(Integer, nullable=False, default=0)  # Number of times rule has been triggered
    last_triggered_at = Column(TIMESTAMP(timezone=True))  # When rule was last triggered
    last_triggered_content = Column(JSON)  # Content that last triggered the rule
    created_by = Column(Text, default="system")  # User who created the rule
    updated_by = Column(Text)  # User who last updated the rule
    description = Column(Text)  # Description/notes about the rule
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class DomainAlert(Base):
    """Track domain-level violations and defederation thresholds"""
    __tablename__ = "domain_alerts"
    id = Column(BigInteger, primary_key=True)
    domain = Column(Text, nullable=False, unique=True)
    violation_count = Column(Integer, nullable=False, default=0)
    last_violation_at = Column(TIMESTAMP(timezone=True))
    defederation_threshold = Column(Integer, nullable=False, default=10)  # Configurable threshold
    is_defederated = Column(Boolean, nullable=False, default=False)
    defederated_at = Column(TIMESTAMP(timezone=True))
    defederated_by = Column(Text)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class ScanSession(Base):
    """Track scanning sessions and progress across multiple users/accounts"""
    __tablename__ = "scan_sessions"
    id = Column(BigInteger, primary_key=True)
    session_type = Column(Text, nullable=False)  # 'local', 'remote', 'federated'
    status = Column(Text, nullable=False, default='active')  # 'active', 'completed', 'paused', 'failed'
    accounts_processed = Column(Integer, nullable=False, default=0)
    total_accounts = Column(Integer)  # Estimated total if known
    current_cursor = Column(Text)  # Current position in the scan
    last_account_id = Column(Text)  # Last processed account ID
    rules_applied = Column(JSON)  # Rules that were active during this session
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True))
    session_metadata = Column(JSON)  # Additional session metadata (renamed from metadata)


class ContentScan(Base):
    """Track individual content scans to prevent re-processing"""
    __tablename__ = "content_scans"
    id = Column(BigInteger, primary_key=True)
    content_hash = Column(Text, nullable=False, unique=True)  # Hash of content being scanned
    mastodon_account_id = Column(Text, nullable=False)
    status_id = Column(Text)  # Optional status ID if scanning specific posts
    scan_type = Column(Text, nullable=False)  # 'account', 'status', 'profile'
    last_scanned_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    scan_result = Column(JSON)  # Store scan results for caching
    rules_version = Column(Text)  # Rules version hash when scanned
    needs_rescan = Column(Boolean, nullable=False, default=False)  # Flag for content that needs re-scanning


class ScheduledAction(Base):
    __tablename__ = "scheduled_actions"
    id = Column(BigInteger, primary_key=True)
    mastodon_account_id = Column(Text, index=True, nullable=False)
    action_to_reverse = Column(sa_Enum('report', 'silence', 'suspend', 'disable', 'sensitive', 'domain_block', name='action_type_enum', create_type=False), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), index=True, nullable=False)


class InteractionHistory(Base):
    __tablename__ = "interaction_history"
    id = Column(BigInteger, primary_key=True)
    source_account_id = Column(Text, nullable=False)
    target_account_id = Column(Text, nullable=False)
    status_id = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class AccountBehaviorMetrics(Base):
    __tablename__ = "account_behavior_metrics"
    id = Column(BigInteger, primary_key=True)
    mastodon_account_id = Column(Text, unique=True, nullable=False)
    posts_last_1h = Column(Integer, default=0)
    posts_last_24h = Column(Integer, default=0)
    last_sampled_status_id = Column(Text)
    last_calculated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(BigInteger, primary_key=True)
    action_type = Column(Text, nullable=False)
    triggered_by_rule_id = Column(BigInteger, ForeignKey('rules.id'), nullable=True)
    target_account_id = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    evidence = Column(JSON)
    api_response = Column(JSON)