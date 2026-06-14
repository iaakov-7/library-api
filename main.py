from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.book_routes import router as book_router
from routes.member_routes import router as member_router
from routes.report_routes import router as report_router
from database.db_connection import db_conn

@asynccontextmanager
async def lifespan():
    db_conn.create_tables()
    yield
    db_conn.close()


app = FastAPI(lifespan=lifespan,title="Library API")

app.include_router(book_router,prefix="/books")
app.include_router(member_router,prefix="/members")
app.include_router(report_router,prefix="/reports")
