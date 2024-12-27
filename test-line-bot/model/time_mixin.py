from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc)


@declarative_mixin
class TimeMixin:
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
