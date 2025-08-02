from sqlalchemy import JSON, TIMESTAMP, BigInteger, Boolean, Column, Numeric, Text
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
    rule_type = Column(Text, nullable=False)  # username_regex, display_name_regex, content_regex
    pattern = Column(Text, nullable=False)
    weight = Column(Numeric, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    is_default = Column(Boolean, nullable=False, default=False)  # True for rules from rules.yml
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
