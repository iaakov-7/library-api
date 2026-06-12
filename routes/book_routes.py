from fastapi import APIRouter
from database.book_db import db_book

router = APIRouter(tags=["books"])


@router.get("")
def get_all_books():
    return db_book.get_all_books()