from pydantic import BaseModel

class UserUpdate(BaseModel):
    name: str
    city_name: str