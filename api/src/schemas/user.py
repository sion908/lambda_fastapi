from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.user import SexType

from .mixin import ForOrm


class UserCreate(BaseModel, ForOrm):
    """Input"""

    username: Optional[str] = None
    password: Optional[str] = None
    sex: Optional[SexType] = Field(None, description="0:男性,1:女性,2:その他")
    age: Optional[int] = None


class OutputUser(BaseModel, ForOrm):
    model_config = ConfigDict(from_attributes=True)
    """Output"""
    id: str = Field(..., description="uuid")
    username: Optional[str]
    sex: Optional[SexType] = Field(..., description="0:男性,1:女性,2:その他")
    age: Optional[int]
