from fastapi import Depends, Query ,File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from utils.auth import *
from configuration.config import *
from .chat_schema import *
from .chat_controller import *
from .chat_model import *

httpbearer = AdminJWT()

@router.get("/chat/getAllchat", tags=["Chat"])
async def getChat(group_id : int,db: Session = Depends(get_session)):
    return getChatController(db,group_id)

@router.get("/chat/getGroupsSharedChat", tags=["Chat"])
async def getGroupsSharedChat(chat_id : int,db: Session = Depends(get_session)):
    return getGroupsSharedChatController(db,chat_id)

@router.post("/chat/createchat",dependencies = [Depends(httpbearer)],  tags=["Chat"], summary="member can send image here")
async def createchat(group_id:int,description: str = Form(...), file: UploadFile = File(...),Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return createChatController(db, Auth_head,group_id, file, description)

@router.post("/chat/shareChat",dependencies = [Depends(httpbearer)],  tags=["Chat"], summary="member can share image here")
async def createchat(chat_id:int,group_id:int,Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return shareChatController(db, Auth_head,group_id,chat_id)

@router.delete("/chat/deleteChat",dependencies = [Depends(httpbearer)],  tags=["Chat"], summary="member can send image here")
async def createchat(chat_id:int,Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return deleteChatController(db, Auth_head,chat_id)
