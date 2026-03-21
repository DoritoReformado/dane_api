from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    _key: str  # en ArangoDB, el _key es el identificador único
    _id: str  # en ArangoDB, el ID es una cadena

    class Config:
        from_attributes = True  # antes era orm_mode = True en Pydantic v1

class InformationTopicBase(BaseModel):
    _key: str  # en ArangoDB, el _key es el identificador único
    _id: str  # en ArangoDB, el ID es una cadena
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True

class InformationTopicCreate(InformationTopicBase):
    pass
    
