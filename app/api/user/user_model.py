from configuration.config import *
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phonenumber = Column(String, unique=True)
    username = Column(String, unique=True)
    bio = Column(String)
    profile_pic = Column(String)
    password = Column(String)
    is_active = Column(Boolean)
    is_deleted = Column(Boolean)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)
    updated_by = Column(Integer)

    User_logs = relationship("User_signin_logs", back_populates="Logs_user")
    User_token = relationship("Tokens", back_populates="Token_user")
    User_group = relationship("Group", back_populates="Group_user")
    User_members = relationship("Members", back_populates="Members_user")
    User_report = relationship("Report", back_populates="Report_user")

class User_signin_logs(Base):
    __tablename__ = "user_logs"

    log_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    logged_in = Column(DateTime)
    logged_out = Column(DateTime)

    Logs_user = relationship("User", back_populates="User_logs")

class Tokens(Base):
    __tablename__ = "tokens"

    token_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    token = Column(String, nullable=False)

    Token_user = relationship("User", back_populates="User_token")
