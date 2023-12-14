from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal

class GroupResponse(BaseModel):
    group_id : int = None
    group_name : str = None
    description : str = None
    creator : int = None
    is_private : bool = None
    is_deleted : bool = None
    deleted_by : int = None
    created_at : datetime = None
    created_by : int = None
    updated_at : Optional[datetime] = None
    updated_by : Optional[int] = None

class CreateGroup(BaseModel):
    group_name : str = None
    description : str = None
    is_private : bool = None
    members : list[int] = None

    class Config:
        json_schema_extra = {
            "example" : {
                "group_name" : "friends forever",
                "description":"This for friends",
                "is_private":False,
                "members":[1,2,3]
            }
        }

class Createreport(BaseModel):
    reason : str = None