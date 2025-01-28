from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated, Optional, Any
from pydantic import (
    BaseModel,
    BeforeValidator,
)

PyObjectId = Annotated[str, BeforeValidator(str)]

class CommonModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_archived:bool=False
    short_name: Optional[str] = Field(default=None)


    created_at: Optional[datetime]=datetime.now()
    updated_at: Optional[datetime]=datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True)

   
class ResponseModel(BaseModel):
    class_name: Optional[str]=None
    data: Any=None
    status_code: int
    number_of_data_items: int
    message: str

    @classmethod
    def create(cls, *, class_name: str="", data: Any=None, status_code: int = 200, message: str = "Success"):
        return cls(
            class_name=class_name,
            data=data,
            status_code=status_code,
            number_of_data_items=len(data) if isinstance(data, (list, tuple)) else 1 if data else 0,
            message=message
        )


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}