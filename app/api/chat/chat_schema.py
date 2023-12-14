from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal
from fastapi import UploadFile

class Createchat(BaseModel):
    description: str
    file: UploadFile