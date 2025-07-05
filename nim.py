import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Показываем все записи из таблицы users
cur.execute("SELECT * FROM users;")
rows = cur.fetchall()

print("Данные из таблицы users:")
for row in rows:
    print(row)

conn.close()