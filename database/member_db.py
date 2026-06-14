from database.db_connection import db_conn

class MemberDB:
    def __init__(self):
        self.db = db_conn

    def create_member(self,date:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """INSERT INTO members(name,email)
        VALUES(%s,%s)""" 
        values = list(date.values())
        cursor.execute(query,values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id
    
    def get_all_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM members"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_member_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM members
        WHERE id=%s"""
        cursor.execute(query,(id,))
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def update_member(self,id:int,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        set_columns = [f"{key}=%s" for key in data.keys()]
        set_clouse = ", ".join(set_columns)
        query = f"""UPDATE members
                SET {set_clouse}
                WHERE id= %s""" 
        values = list(data.values())
        cursor.execute(query,(values+[id]))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated
    
    def deactivate_member(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        query = """UPDATE members
        SET is_active=FALSE
        WHERE id=%s"""
        cursor.execute(query,(id,))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated  

    def activate_member(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        query = """UPDATE members
        SET is_active=TRUE
        WHERE id=%s"""
        cursor.execute(query,(id,))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated 

    def increment_borrows(self,id:int):               
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        query = """UPDATE members
        SET total_borrows=total_borrows + 1
        WHERE id=%s"""
        cursor.execute(query,(id,))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated 
    
    def count_active_members(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(*) AS num_active
        FROM members
        WHERE is_active = TRUE"""
        cursor.execute(query)
        count = cursor.fetchone()
        cursor.close()
        return count 
    
    def get_top_member(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT id AS member_id, total_borrows AS borrowed FROM members 
        WHERE total_borrows= (SELECT MAX(total_borrows) FROM members)"""
        cursor.execute(query)
        top_member = cursor.fetchall()
        cursor.close()
        return top_member       



db_member = MemberDB()

   