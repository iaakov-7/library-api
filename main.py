from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.book_routes import router as book_router
from database.db_connection import db_conn

@asynccontextmanager
async def lifespan(app:FastAPI):
    db_conn.create_tables()
    yield
    db_conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(book_router,prefix="/books")