from pydantic import BaseModel
from enum import Enum


class Genre(str,Enum):
    FICTION = "Fiction"  
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science" 
    HISTORY = "History"  
    OTHER = "Other" 

class Book(BaseModel):
    title:str
    author:str
    genre:Genre


class UpdateBook(BaseModel):
    title:str | None = None
    author:str | None = None
    genre:Genre | None = None  

class Member(BaseModel):  
    name:str
    email:str  

class UpdateMember(BaseModel):
    name:str | None = None
    email:str | None = None             