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
    is_deleted = Column(Boolean,nullable= False, default=False)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)
    updated_by = Column(Integer)

    Group_user = relationship("User", back_populates="User_group")
    Group_members = relationship("Members", back_populates="Members_group")
    Group_report = relationship("Report",back_populates="Report_group")

class Members(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    group_id = Column(Integer, ForeignKey("group.group_id"))
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean,nullable= False, default=False)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)
    updated_by = Column(Integer)

    Members_user = relationship("User", back_populates="User_members")
    Members_group = relationship("Group", back_populates="Group_members")
    Member_admin = relationship("GroupAdmin", back_populates="Admin_member")

class GroupAdmin(Base):
    __tablename__ = "groupadmin"

    admin_id = Column(Integer, primary_key=True,unique=True, index=True)
    group_id = Column(Integer, ForeignKey("group.group_id"))
    member_id = Column(Integer, ForeignKey("members.member_id"))
    is_deleted = Column(Boolean,nullable= False, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Admin_group = relationship("Group",back_populates="Group_admin")
    Admin_member = relationship("Members",back_populates="Member_admin")

class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    group_id = Column(Integer, ForeignKey("group.group_id"))
    report_type = Column(String, nullable=False)
    report = Column(String, nullable=False)
    reported_at = Column(DateTime, nullable=False)

    Report_group = relationship("Group", back_populates="Group_report")
    Report_user = relationship("User", back_populates="User_report")



