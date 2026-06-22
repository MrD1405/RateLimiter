from database import Database

database=Database()

database.make_db_connection()

data=database.cursor.execute('SELECT * FROM users')
print(database.cursor.fetchall())