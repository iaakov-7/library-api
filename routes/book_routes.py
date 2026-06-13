from fastapi import APIRouter
from database.book_db import db_book
from logs.logger_config import logger

router = APIRouter(tags=["books"])


@router.get("")
def get_all_books():
    all_books = db_book.get_all_books()
    if len(all_books) == 0:
        logger.warning("Three are no books in the library")
    return all_books    
