import sqlite3

# Настройка пути к базе данных
DATABASE_PATH = r'C:\FLASK\DPO PORTAL\database.db'

def connect_to_db():
    try:
        connection = sqlite3.connect('database.db')
        print("База данных открыта успешно.")
        return connection
    except sqlite3.Error as e:
        print(f"Ошибка при соединении с базой данных: {e}")
        exit(1)

def fetch_institutions(connection):
    c = connection.cursor()
    c.execute('''SELECT * FROM institutions''')
    rows = c.fetchall()
    if len(rows) == 0:
        print("Таблица institutions пустая.")
    else:
        for row in rows:
            print(row)

def main():
    connection = connect_to_db()
    fetch_institutions(connection)
    connection.close()

if __name__ == '__main__':
    main()