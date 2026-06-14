from database.db_connection import db_conn

class BookDB:
    def __init__(self):
        self.db = db_conn

    def create_book(self,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """INSERT INTO books(title,author,genre)
        VALUES(%s,%s,%s)"""
        values = list(data.values()) 
        cursor.execute(query,values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id

    def get_all_books(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM books"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()    
        return rows
    
    def get_book_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM books WHERE id=%s"""
        cursor.execute(query,(id,))
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def update_book(self,id:int,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        set_columns = [f"{key}=%s" for key in data.keys()]
        set_clouse = ", ".join(set_columns)
        query = f"""UPDATE books
                SET {set_clouse}
                WHERE id= %s""" 
        values = list(data.values())
        cursor.execute(query,values+[id]) 
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated   

    def set_available(self,id:int,value:bool,member_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """UPDATE books
                SET is_available=%s,
                borrowed_by_member_id=%s
                WHERE id=%s"""
        cursor.execute(query,(value,member_id,id))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated
    
    def count_total_books(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS total_books 
        FROM books""" 
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row  

    def count_available_books(self):     
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS num_available_books 
        FROM books
        WHERE is_available= TRUE""" 
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row 

    def count_borrowed_books(self):  
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS num_borrowed_books 
        FROM books
        WHERE is_available= FAlSE""" 
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row 

    def count_by_genre(self):  
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT genre, COUNT(*) AS count 
                    FROM books 
                 GROUP BY genre
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def count_active_borrows_by_member(self,member_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS total
        FROM books
        WHERE borrowed_by_member_id=%s"""
        cursor.execute(query,(member_id,))
        row = cursor.fetchone()
        cursor.close()
        return row
    


db_book = BookDB()


