import mysql.connector

class DBconnection:
    def __init__(self):
            self.connect()
            
            
    def connect(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",password="root",database="library_db")
        
    
    def get_connection(self):
        if not self.connection.is_connected():
            self.connect()
        return self.connection    
    
    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(50) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    genre ENUM('Fiction','Non-Fiction','Science','History','Other') NOT NULL,
                    is_available BOOLEAN DEFAULT TRUE NOT NULL,
                    borrowed_by_member_id INT )""")
        connection.commit()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS members(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    total_borrows INT NOT NULL DEFAULT 0)""")
        connection.commit() 
        cursor.close()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed successfully")  
        else:
            print("Database connection was already closed")       

db_conn = DBconnection()