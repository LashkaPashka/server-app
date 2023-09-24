from pydantic import EmailStr, BaseModel


class SAuth(BaseModel):
    email: EmailStr
    password: str







