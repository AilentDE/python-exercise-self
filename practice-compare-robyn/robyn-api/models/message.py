from sqlalchemy import Uuid, Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base
from uuid import uuid4

from models.time_mixin import TimeMixin


class MessagePremission(Base):
    __tablename__ = "message_premission"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    level = Column(Integer, unique=True)
    description = Column(String, default="")

    def __repr__(self):
        return f"<MessagePremission(id={self.id}, level={self.level}, description={self.description})>"

    @staticmethod
    def base_premission():
        return [
            MessagePremission(level=0, description="Public"),
            MessagePremission(level=1, description="Protected"),
            MessagePremission(level=2, description="Private"),
        ]


class Message(Base, TimeMixin):
    __tablename__ = "messages"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    author_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    content = Column(String)
    permission_level = Column(Integer, ForeignKey("message_premission.level"))
    history = relationship("ReadHistory", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Message(id={self.id}, author_id={self.author_id}, "
            f"title={self.title}, content={self.content}, "
            f"permission_level={self.permission_level})>"
        )


class ReadHistory(Base, TimeMixin):
    __tablename__ = "read_history"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"))
    message_id = Column(Uuid(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"))
    __table_args__ = (UniqueConstraint("user_id", "message_id", name="uq_user_message"),)
    message = relationship("Message", back_populates="history")

    def __repr__(self):
        return f"<ReadHistory(id={self.id}, user_id={self.user_id}, message_id={self.message_id})>"
