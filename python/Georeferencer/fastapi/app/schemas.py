from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    _key: str  # en ArangoDB, el _key es el identificador único
    id: str = Field(alias="_id")

    class Config:
        from_attributes = True  # antes era orm_mode = True en Pydantic v1

class InformationTopicBase(BaseModel):
    _key: str  # en ArangoDB, el _key es el identificador único
    id: str = Field(alias="_id")
    name: str
    description: str | None = None
    subtopics: list = Field(default_factory=list)  # Lista de subtopics, por ahora vacía
    class Config:
        from_attributes = True

class InformationTopicCreate(InformationTopicBase):
    pass
    
class InformationTopicUpdate(BaseModel):
    """Schema para actualizaciones PARCIALES (PATCH)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)

class SubInformationTopicBase(BaseModel):
    _key: str
    id: str = Field(alias="_id") 
    topic_id: str
    name: str
    description: str | None = None
    information_topic: Optional[InformationTopicBase] | None = None  # Para incluir info del topic padre
    datasets: list = Field(default_factory=list) # Lista de datasets, por ahora vacía
    
    class Config:
        from_attributes = True

class SubInformationTopicCreate(BaseModel):
    topic_id: dict
    name: str
    description: str | None = None
    
class SubInformationTopicUpdate(BaseModel):
    """Schema para actualizaciones PARCIALES (PATCH)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)