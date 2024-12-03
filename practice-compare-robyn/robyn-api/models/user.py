from sqlalchemy import Uuid, Column, String, ForeignKey, UniqueConstraint
from config.database import Base
from uuid import uuid4

from models.time_mixin import TimeMixin
from utils.hash_handler import get_password_hash, verify_password


class User(Base, TimeMixin):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, hashed_password={self.password}, email={self.email})>"

    def hash_password(self):
        self.password = get_password_hash(self.password)

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)


class UserSubscriptions(Base, TimeMixin):
    __tablename__ = "user_subscriptions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    author_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    # 保留id字段使用的unique约束，但是不会创建索引
    # 也可以使用雙主鍵來省略id字段
    __table_args__ = (UniqueConstraint("user_id", "author_id", name="uq_user_author"),)

    def __repr__(self):
        return f"<UserSubscriptions(id={self.id}, user_id={self.user_id}, author_id={self.author_id})>"
