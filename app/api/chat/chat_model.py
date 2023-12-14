from configuration.config import *
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class Chat(Base):
    __tablename__ = "chat"

    chat_id = Column(Integer,primary_key=True, unique=True, index=True)
    member_id = Column(Integer, ForeignKey("members.member_id"))
    group_id = Column(Integer, ForeignKey("group.group_id"))
    image = Column(String, nullable=False)
    is_shared = Column(Boolean, default=False)
    shared_chat_id = Column(Integer,ForeignKey("chat.chat_id"))
    shared_count = Column(Integer, default=0)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(Integer)
    updated_by = Column(Integer)