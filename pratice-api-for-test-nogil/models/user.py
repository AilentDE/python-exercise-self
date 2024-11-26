from config.db_postgres import Base
from sqlalchemy import Uuid, Column, String, Boolean, DateTime
from uuid import uuid4

from utils.time_helper import utc_now


class User(Base):
    __tablename__ = "users"

    uuid = Column(Uuid(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now)
    deleted_at = Column(DateTime(timezone=True), default=utc_now)

    def __repr__(self):
        return f"<User {self.username}>"
