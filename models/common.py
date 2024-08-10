from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated, Optional
from pydantic import (
    BaseModel,
    BeforeValidator,
)

PyObjectId = Annotated[str, BeforeValidator(str)]

class CommonModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_archived:bool=False

    created_at: Optional[datetime]=datetime.now()
    updated_at: Optional[datetime]=datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True)

   
def ResponseModel(data:dict={}, message:str='',code:Optional[int]=200):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}