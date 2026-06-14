from fastapi import APIRouter,HTTPException
from database.book_db import db_book
from database.member_db import db_member
from logs.logger_config import logger

router = APIRouter(tags=["Reports"])

@router.get("/summary")
def get_general_report():
    logger.info("Incoming request: get general available")
    general = {
        "total_books":db_book.count_total_books().get("total_books"),
        "available_books":db_book.count_available_books().get("num_available_books"),
        "currently_borrowed":db_book.count_borrowed_books().get("num_borrowed_books"),
        "active_members":db_member.count_active_members().get("num_active")
    }
    logger.info("Rwaded general report")
    return general

@router.get("/books-by-genre")
def get_books_genre():
    logger.info("Incoming request: get genres")
    count_genres = db_book.count_by_genre()
    logger.info("Readed count by genre")
    return count_genres

@router.get("/top-member")
def top_member():
    logger.info("Incoming request: get top member")
    top_member = db_member.get_top_member()
    logger.info("Readed top member")
    return top_member