from pydantic import Field
from pymongo import ASCENDING, IndexModel
from models.common import CommonModel


class Material(CommonModel):
   name:str=Field(..., min_length=3, max_length=50)
   class Settings:
        name = "mateerials"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True),
            IndexModel([("short_name", ASCENDING)], unique=True)
        ]

