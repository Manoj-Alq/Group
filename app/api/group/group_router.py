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
async def getAllbook(search: str = Query("", description="Search by title or author"),page: int = Query(1, gt=0, description="Page number"),
    page_size: int = Query(10, gt=0, lt=101, description="Number of items per page"),genre: str = Query("", description="Filter by genre"),
    publication_year: int = Query(0, description="Filter by publication year"),db: Session = Depends(get_session)):
    return getAllGroupController(db,search,page,page_size,publication_year,genre)

# @router.get("/group/getagroup/{id}",response_model=groupresponse, tags=["group"])
# async def getSinglebook(id:int,db: Session = Depends(get_session)):
#     return getSinglegroupController(db, id) 

# @router.post("/group/creategroup",dependencies = [Depends(httpbearer)], response_model=groupresponse, tags=["group"], summary="author can signup here")
# async def createbook(book: Create_book,role:str = Depends(author_admin_authorization),db: Session = Depends(get_session)):
#     return createBookController(db, book)

# @router.post("/group/updategroup",dependencies = [Depends(httpbearer)],response_model=groupresponse, tags=["group"])
# async def updatebook(book: Create_book,id:int,role:str = Depends(author_admin_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
#     return updatebookController(db,book, id)

# @router.post("/group/deletegroup",dependencies = [Depends(httpbearer)],response_model=groupresponse, tags=["group"])
# async def signupbook(id:int = None,role:str = Depends(author_admin_authorization),Auth_head:str = Depends(get_authorization_header),db: Session = Depends(get_session)):
#     return deletebookController(db, Auth_head, id)