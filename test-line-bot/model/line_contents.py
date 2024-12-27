from sqlalchemy import Column, Integer, String

from config.database import Base
from model.time_mixin import TimeMixin


class LineContents(Base, TimeMixin):
    __tablename__ = "line_contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_type = Column(String, nullable=False)
    content_id = Column(String, nullable=False)
