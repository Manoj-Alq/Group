from .user_schema import *
from fastapi import Depends
from sqlalchemy.orm import Session
from .user_controller import *
from typing import List
from utils.auth import *
from configuration.config import *
from .user_model import *

httpbearer = AdminJWT()

@router.get("/user/get", tags=["User"])
async def getUser(id:int = None, db: Session = Depends(get_session) ):
    return getUserController(db, id)

@router.post("/user/create",response_model=UserResponse, tags=["User"])
async def createUser(user : CreateUserSchema, db: Session = Depends(get_session) ):
    return createUserController(db,user)

@router.post("/user/logininuser/",  tags=["User"], summary="users can signin here")
async def logInuser(user: LoginUser,db: Session = Depends(get_session)):
    return logInuserController(db,user)

@router.get("/user/getMyProfile/",dependencies = [Depends(httpbearer)],response_model=UserResponse,  tags=["User"], summary="users can get their profile here")
async def getMyProfile(Auth_head:str = Depends(get_authorization_header),role : str = Depends(user_authorization),db: Session = Depends(get_session)):
    return getMyProfileController(db,Auth_head)

@router.put("/user/updateuser",dependencies = [Depends(httpbearer)], response_model=UserResponse, tags=["User"], summary="user can update their details here")
async def updateuser(id:int,user: CreateUserSchema,Auth_head:str = Depends(get_authorization_header),x : str = Depends(user_authorization),db: Session = Depends(get_session)):
    return updateUserController(db,user,Auth_head,id)

@router.post("/user/logoutuser/",dependencies = [Depends(httpbearer)], tags=["User"], summary="user can signout here")
async def signoutuser(id:int=None,Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return logoutuserController(db,Auth_head,id)

@router.delete("/user/deleteuser",dependencies = [Depends(httpbearer)], response_model=UserResponse, tags=["User"], summary="user can delete their account here")
async def deleteuser(id:int=None,Auth_head:str = Depends(get_authorization_header),role:str = Depends(user_authorization),db: Session = Depends(get_session)):
    return deleteUserController(db,Auth_head,id)