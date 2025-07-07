import sqlite3
from werkzeug.security import generate_password_hash

def create_admin_user():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    username = 'admin'
    password = '12345'  # Замените на нужный пароль
    hashed_password = generate_password_hash(password)

    first_name = 'Admin'
    last_name = 'User'
    email = 'admin19@example.com'

    # Пример вставки пользователя с ролью администратора
    cursor.execute('''
        INSERT INTO users (username, password, first_name, last_name, email, role_admin)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, hashed_password, first_name, last_name, email, True))

    conn.commit()
    conn.close()
    print("Admin user created successfully.")

if __name__ == '__main__':
    create_admin_user()
