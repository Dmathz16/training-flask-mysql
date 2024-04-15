import pymysql

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'training_python_flask'

db = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)

cursor = db.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(191) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")

cursor.execute("DROP TABLE IF EXISTS posts")
cursor.execute("""
    CREATE TABLE posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        author_id INT NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES user (id)
    )
""")

cursor.close()
db.close()
