from db_connection import db_conn

class MemberDB:
    def __init__(self):
        self.db = db_conn

    def create_member(self,date:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        quary = """INSERT INTO members(name,email)
        VALUES(%s,%s)""" 
        values = list(date.values())
        cursor.execute(quary,values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id
    
    def get_all_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        quary = """SELECT * FROM members"""
        cursor.execute(quary)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_member_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        quary = """SELECT * FROM members
        WHERE id=%s"""
        cursor.execute(quary,(id,))
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def update_member(self,id:int,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        set_columns = [f"{key}=%s" for key in data.keys()]
        set_clouse = ", ".join(set_columns)
        quary = f"""UPDATE members
                SET {set_clouse}
                WHERE id= %s""" 
        values = list(data.values())
        cursor.execute(quary,(values+[id]))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated
    
    def deactivate_member(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        quary = """UPDATE members
        SET is_active=FALSE
        WHERE id=%s"""
        cursor.execute(quary,(id,))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated  

    def activate_member(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        quary = """UPDATE members
        SET is_active=TRUE
        WHERE id=%s"""
        cursor.execute(quary,(id,))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated 

    def increment_borrows(self,id:int):               
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        quary = """SELECT total_borrows FROM members
        WHERE id= %s"""
        cursor.execute(quary,(id,))
        total_borrows= cursor.fetchone()[0]+1
        quary = """UPDATE members
        SET total_borrows=%s
        WHERE id=%s"""
        cursor.execute(quary,(total_borrows,id))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated 
    
    def count_active_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        quary = """SELECT COUNT(*) AS num_active
        FROM members
        WHERE is_active = TRUE"""
        cursor.execute(quary)
        count = cursor.fetchone()
        cursor.close()
        return count 
    
    def get_top_member(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT MAX(total_borrows) FROM members""")
        max_borrows = cursor.fetchone()["MAX(total_borrows)"]
        quary = """SELECT * FROM members
        WHERE total_borrows=%s"""
        cursor.execute(quary,(max_borrows,))
        top_member = cursor.fetchone()
        cursor.close()
        return top_member       



member = MemberDB()
   