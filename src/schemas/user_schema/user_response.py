from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True