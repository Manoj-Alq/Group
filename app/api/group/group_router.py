from fastapi import Depends, Query
from sqlalchemy.orm import Session
from typing import List
from utils.auth import *
from configuration.config import *
from .group_schema import *
from .group_controller import *
from .group_model import *

httpbearer = AdminJWT()

@router.get("/group/getAllgroup", tags=["group"])
async def getGroup(group_id : int = None,db: Session = Depends(get_session)):
    return getGroupController(db,group_id)

@router.post("/group/creategroup",dependencies = [Depends(httpbearer)],  tags=["group"], summary="author can signup here")
async def creategroup(group: CreateGroup,Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return createGroupController(db, group, Auth_head)

@router.put("/group/updategroup",dependencies = [Depends(httpbearer)], tags=["group"])
async def updategroup(group: CreateGroup,group_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return updateGroupController(db,group, group_id, Auth_head)

@router.delete("/group/deletegroup",dependencies = [Depends(httpbearer)],response_model=GroupResponse, tags=["group"])
async def deleteGroup(group_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return deleteGroupController(db, Auth_head, group_id)

@router.post("/group/addmember",dependencies = [Depends(httpbearer)], tags=["group"])
async def addMember(group_id:int,user_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return addMemberController(db, Auth_head, group_id, user_id)

@router.delete("/group/deleteMember",dependencies = [Depends(httpbearer)], tags=["group"])
async def addMember(group_id:int,member_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return deleteMemberController(db, Auth_head, group_id, member_id)

@router.post("/group/report",dependencies = [Depends(httpbearer)], tags=["group"])
async def reportgroup(group_id:int,report: Createreport,report_type: str = Query("spam", enum=["spam", "uncomfortable for group", "other"]),role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return reportGroupController(db, Auth_head, group_id, report, report_type)

@router.post("/group/promoteAdmin",dependencies = [Depends(httpbearer)], tags=["group"])
async def promoteAdmin(member_id:int,group_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return promoteAdminController(db, Auth_head, group_id,member_id)

@router.post("/group/depromoteAdmin",dependencies = [Depends(httpbearer)], tags=["group"])
async def depromoteAdmin(member_id:int,group_id:int,role:str = Depends(user_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
    return depromoteAdminController(db, Auth_head, group_id,member_id)

