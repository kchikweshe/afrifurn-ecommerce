from pydantic import Field
from models.common import CommonModel


class Material(CommonModel):
   name:str=Field(..., min_length=3, max_length=50)
   

