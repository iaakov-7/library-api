from fastapi import APIRouter
from database.book_db import db_book
from database.member_db import db_member

router = APIRouter(tags=["Reports"])

@router.get("/summary")
def get_general_report():
    return {
        "total_books":db_book.count_total_books().get("total_books"),
        "available_books":db_book.count_available_books().get("num_available_books"),
        "currently_borrowed":db_book.count_borrowed_books().get("num_borrowed_books"),
        "active_members":db_member.count_active_members().get("num_active")

    }

@router.get("/books-by-genre")
def get_books_genre():
    return db_book.count_by_genre()

@router.get("/top-member")
def top_member():
    return db_member.get_top_member()