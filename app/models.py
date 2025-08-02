from sqlalchemy import JSON, TIMESTAMP, BigInteger, Column, Numeric, Text
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
