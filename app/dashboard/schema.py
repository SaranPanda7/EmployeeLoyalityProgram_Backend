
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID4, Json


class SchemaUserRewardCount(BaseModel):

    title:  str = None
    id:  str = None
    count: str = None

class SchemaTopPerformance(BaseModel):
    title: str = None
    id: str = None
    points: int = None

class SchemaBanner(BaseModel):
    title : Optional[str]
    image : Optional[str]
    start_date : Any
    end_date : Any

    class Config:
        orm_mode = True


class CreateSchemaBanner(BaseModel):
    title: str= None
    image: str= None
    start_date: str= None
    end_date: str= None

class UpdateSchemaBanner(BaseModel):
    # id:  str = None
    title : str= None
    image: str=None



class SchemaPerformer(BaseModel):
    
    first_name: str = None
    sum: int = None

class SchemaGetAllImages(BaseModel):
    
    title : Optional[str]
    image_url : Optional[str]





