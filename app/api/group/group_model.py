from configuration.config import *
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class Group(Base):
    __tablename__ = "group"

    group_id = Column(Integer, primary_key=True, unique=True, index=True)
    group_name = Column(String)
    description = Column(String)
    creator = Column(Integer, ForeignKey("user.user_id"))
    is_private = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean,nullable= False)
    deleted_by = Column(Integer,ForeignKey("user.user_id"))
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer,ForeignKey("user.user_id"))

    Group_user = relationship("User", back_populates="User_group")

class Members(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    is_deleted = Column(Boolean,nullable= False)
    deleted_by = Column(Integer,ForeignKey("user.user_id"))
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_at = Column(DateTime)
    updated_by = Column(Integer,ForeignKey("user.user_id"))

    Members_user = relationship("User", back_populates="User_members")


