import sqlite3

# Настройка пути к базе данных
DATABASE_PATH = 'database.db'  # Замените на настоящий путь к вашей базе данных

def connect_to_db():
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        return connection
    except sqlite3.Error as e:
        print(f"Ошибка при соединении с базой данных: {e}")
        exit(1)

def insert_into_institutions(connection):
    data = [
        ('МГУ', 'Московский государственный университет имени М.В. Ломоносова'),
        ('СПбГУ', 'Санкт-Петербургский государственный университет'),
        ('НГУ', 'Новосибирский государственный университет'),
        ('РУДН', 'Российский университет дружбы народов'),
        ('МФТИ', 'Московский физико-технический институт')
    ]
    
    cursor = connection.cursor()
    cursor.executemany(
        '''
        INSERT INTO institutions(short_name, full_name) VALUES (?, ?)
        ''',
        data
    )
    connection.commit()
    print("Данные успешно добавлены в таблицу institutions.")

def main():
    connection = connect_to_db()
    insert_into_institutions(connection)
    connection.close()

if __name__ == '__main__':
    main()