import mysql.connector

def get_connection():
    connection = mysql.connector.connect(host="localhost",user="root",password="root",database="library_db")
    return connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   title VARCHAR(50) NOT NULL,
                   author VARCHAR(50) NOT NULL,
                   genre ENUM('Fiction','Non-Fiction','Science','History','Other') NOT NULL,
                   is_available BOOLEAN DEFAULT TRUE NOT NULL,
                   borrowed_by_member_id INT )""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS members(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(50) NOT NULL,
                   email VARCHAR(255) UNIQUE NOT NULL,
                   is_active BOOLEAN DEFAULT TRUE NOT NULL,
                   total_borrows INT NOT NULL)""")
    conn.commit()    