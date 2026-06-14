# library-api

## System description
The system manages books and library members, It receives HTTP requests by
FastAPI server that connect to mysql database.

## Docker
docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8

## Folder structure
```
library-api/ 
│ 
│ 
├── main.py 
├── database/ 
│   ├── db_connection.py 
│   ├── book_db.py 
│   └── member_db.py 
├── routes/ 
│   ├── book_routes.py 
│   ├── member_routes.py 
│   └── report_routes.py 
├── logs/ 
│   └── app.log 
│   └── logger_config.py
├── utils/
|    └── models.py
├── README.md 
├── requirements.txt 
└── .gitignore
```

## Tables structure

### books
```
id: int   
title: varchar
auther: varchar
genre: enum(Action | Science | History | Other )
is_availble: boolean
borrowed_by_member_id: int
```
### Members structure 
```
id: int 
name: varchar 
email: text
is_active: boolean
total_borrows: int
```

## System rules
1. Crete book - User send title+author+genre, System adds is_available=True, borrowed_by=NULL.

2. Genre - Must be Fiction / Non-Fiction / Science / History / Other(valid in post and in patch).

3. Create member - user send name+email, System adds  ,is_active = True, total_borrows = 0.

4. Email - Must be uniqe if exists return error.

5. Member not active - If is_active=False it not possible to borrow a book.

6. Book not available - It not possible to borrow a book that already borrowed (is_available=False).

7. Max number of books - Member cannot hold more than 3 books at a time.

8. Returning a book - A book can only be returned if it is lent to the same friend who is returning it.

##  Endpoints
### Books
```
post.('/books') = create book
get.('/books') = all books
get.('/books/{id}') = book by id
patch.('/books/{id}') = update book
patch.('/books/{id}/borrow/{member_id}') = borrow to member
patch.('/books/{id}/return/{member_id}') = return book by member 
```
### Members
```
post.('/members') = create member
get.('/members') = all members
get.('members/{id}') = member by id
patch.('members/{id}') = update member
patch.('members/{id}/deactivate') = deactivate member
patch.('members/{id}/activate') = activate member
```
### Reports 
```
get.('/reports/summary') = general report
get.('/reports/books-by-genre') = books by genre
get.('/reports/top-member') = the most activate member
```
## System flow
Client want to borrow a book -> check if member is active-> check if member has reached maximum borrows ->
check if book is available -> book is borrowed, Client want to return a book -> check if the book is lent to the member who want to return it -> Book returned.

## How to run
uvicorn main:app

