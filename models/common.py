import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from bson import ObjectId
from typing import Annotated, Optional
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    PlainValidator,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)

PyObjectId = Annotated[str, BeforeValidator(str)]

class CommonModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

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