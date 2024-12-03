from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from datetime import datetime, timezone


def utc_now():
    return datetime.now(tz=timezone.utc)


@declarative_mixin
class TimeMixin:
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False, onupdate=datetime.now)
