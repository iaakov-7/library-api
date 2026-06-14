from fastapi import APIRouter, HTTPException
from database.book_db import db_book
from database.member_db import db_member
from logs.logger_config import logger
from utils.models import Book,UpdateBook

router = APIRouter(tags=["Books"])


@router.get("")
def get_all_books():
    logger.info("Incoming request: get all books")
    all_books = db_book.get_all_books()
    if len(all_books) == 0:
        logger.warning("There are no books in the library")
    logger.info("Reed all books successfully")    
    return all_books

@router.get("/{id}")
def get_book_by_id(id:int):
    logger.info("Incoming request: get book by id")
    book = db_book.get_book_by_id(id)
    if not book:
        logger.error("Book %s not found",id)
        raise HTTPException(404,f"Book with id {id} not found")
    logger.info("Reed book %s successfully",id) 
    return book

@router.post("",status_code=201)
def create_book(new_book:Book):
    logger.info("Incoming request: create book")
    book = new_book.model_dump()
    new_id_book =db_book.create_book(book)
    logger.info("Create book %s successfully",id)
    return {"Success":f"Create a book with id {new_id_book}"}

@router.patch("/{id}")
def update_book(id:int,to_update:UpdateBook):
    logger.info("Incoming request: update book %s",id)
    if not db_book.get_book_by_id(id):
        logger.error("Book %s not found",id)
        raise HTTPException(404,f"Book with id:{id} not found")
    toupdate = to_update.model_dump(exclude_unset=True)
    updated_book = db_book.update_book(id,toupdate)
    if not updated_book:
        raise HTTPException(400,"Bad request")
    return {"Success":f"Book with id {id} updated successfully"}

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id:int,member_id:int):
    logger.info("Incoming request: borrow book %s by member %s",id,member_id)
    book = db_book.get_book_by_id(id)
    member = db_member.get_member_by_id(member_id)
    if not book:
        logger.error("Book %s is not found",id)
        raise HTTPException(404,f"Book with id {id} not found")
    if not member:
        logger.error("Member %s not found",member_id)
        raise HTTPException(404,f"Member with id {member_id} not found")
    if book["is_available"] == False:
        logger.error("Book with id %s not available",id)
        raise HTTPException(400,"Book is not available")
    if member["is_active"] == False:
        logger.error("Member %s not active",member_id)
        raise HTTPException(400," Member is not active")
    if db_book.count_active_borrows_by_member(member_id)["total"] >=3:
        logger.error("Member %s has reached maximum borrows",member_id)
        raise HTTPException(400, "Member has reached maximum borrows") 
    db_book.set_available(id,False,member_id)
    db_member.increment_borrows(member_id)
    logger.info("Success: borrowed book %s by member %s",id,member_id)
    return {"Success":f"book with id {id} has borrowed to member with id {member_id}"}      

@router.patch("/{id}/return/{member_id}")
def return_book(id:int,member_id:int):
    logger.info("Incoming request: return book %s by member %s",id,member_id)
    book = db_book.get_book_by_id(id)
    member = db_member.get_member_by_id(member_id)
    if not book:
        logger.error("Book %s is not found",id)
        raise HTTPException(404,f"Book with id {id} not found")
    if not member:
        logger.error("Member %s not found",member_id)
        raise HTTPException(404,f"Member with id {member_id} not found")
    if book["is_available"] == True:
        logger.error("Book %s is not borrowed",id)
        raise HTTPException(400,"Book is not borrowed")
    if not book["borrowed_by_member_id"] == member_id:
        logger.error("book %s is not borrowed by this member",id)
        raise HTTPException(400,"book is not borrowed by this member")
    db_book.set_available(id,True,None)
    logger.info("Sucess: returned book %s by member %s",id,member_id)
    return {"Success":f"Book with id {id} return by member with id {member_id}"}