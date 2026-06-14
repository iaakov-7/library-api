from fastapi import APIRouter, HTTPException
from database.book_db import db_book
from database.member_db import db_member
from logs.logger_config import logger
from utils.models import Book,UpdateBook

router = APIRouter(tags=["books"])


@router.get("")
def get_all_books():
    all_books = db_book.get_all_books()
    if len(all_books) == 0:
        logger.warning("There are no books in the library")
    return all_books

@router.get("/{id}")
def get_book_by_id(id:int):
    book = db_book.get_book_by_id(id)
    if not book:
        raise HTTPException(404,"Book with id:{id} not found")
    return book

@router.post("",status_code=201)
def create_book(new_book:Book):
    book = new_book.model_dump()
    new_id_book =db_book.create_book(book)
    return {"Success":f"Create a book with id {new_id_book}"}

@router.patch("/{id}")
def update_book(id:int,to_update:UpdateBook):
    if not db_book.get_book_by_id(id):
        raise HTTPException(404,"Book with id:{id} not found")
    toupdate = to_update.model_dump(exclude_unset=True)
    updated_book = db_book.update_book(id,toupdate)
    if not updated_book:
        raise HTTPException(400,"Bad request")
    return {"Success":f"Book with id {id} updated successfully"}

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id:int,member_id:int):
    book = db_book.get_book_by_id(id)
    member = db_member.get_member_by_id(member_id)
    if not book:
        raise HTTPException(404,f"Book with id {id} not found")
    if not member:
        raise HTTPException(404,f"Member with id {member_id} not found")
    if book["is_available"] == False:
        raise HTTPException(400,"Book is not available")
    if member["is_active"] == False:
        raise HTTPException(400," Member is not active")
    if db_book.count_active_borrows_by_member(member_id)["total"] >=3:
        raise HTTPException(400, "Member has reached maximum borrows") 
    db_book.set_available(id,False,member_id)
    db_member.increment_borrows(member_id)
    return {"Success":f"book with id {id} has borrowed to member with id {member_id}"}      

@router.patch("/{id}/return/{member_id}")
def return_book(id:int,member_id:int):
    book = db_book.get_book_by_id(id)
    member = db_member.get_member_by_id(member_id)
    if not book:
        raise HTTPException(404,f"Book with id {id} not found")
    if not member:
        raise HTTPException(404,f"Member with id {member_id} not found")
    if book["is_available"] == True:
        raise HTTPException(400,"Book is not borrowed")
    if not book["borrowed_by_member_id"] == member_id:
        raise HTTPException(400,"book is not borrowed by this member")
    db_book.set_available(id,True,None)
    return {"Success":f"Book with id {id} return by member with id {member_id}"}