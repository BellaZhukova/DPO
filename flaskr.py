import sqlite3              # Библиотека для работы с SQLite
import os                   # Стандартная библиотека для взаимодействия с операционной системой
import smtplib
import json
import secrets
from email.message import EmailMessage
from flask import Flask, Blueprint, current_app, request, session, g, redirect, url_for, render_template, flash, jsonify
from werkzeug.security import check_password_hash  # Безопасное сравнение паролей
from datetime import datetime, timedelta
from werkzeug.exceptions import abort


# Создаем экземпляр приложения Flask
app = Flask(__name__)



# Конфигурация
DATABASE = r'C:\FLASK\DPO PORTAL\database.db'  # Путь к базе данных SQLite
DEBUG = True                 # Включаем режим отладки
SECRET_KEY = 'development key'  # Секретный ключ для сессии

app.config.from_object(__name__)  # Загружаем конфигурацию из этого файла

# Соединение с базой данных
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Результат будет представлен в виде словаря
    return conn

# Получение соединения с базой данных
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r', encoding='utf-8') as f:
            sql_script = f.read().replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
            db.cursor().executescript(sql_script)
        db.commit()

# Инициализация базы данных при первом запуске
init_db()



# Главная страница + обработка формы
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"Пользователь пытается войти с логином: {username}, пароль: {password}")

        # Проверяем введенный логин и пароль
        db = get_db()
        cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        
        if user_data is None or user_data['password'] != password:
            error = 'Неверный логин или пароль.'
        else:
            session['logged_in'] = True
            session['user_id'] = user_data['user_id']
            return redirect(url_for('vhod_vibor'))  # Перенаправляем на страницу vhodVibor.html
    
    return render_template('index.html', error=error)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()

# Страница выбора после авторизации
@app.route('/vhod-vibor')
def vhod_vibor():
    if 'logged_in' in session and session['logged_in']:
        return render_template('vhodVibor.html')
    else:
        return redirect(url_for('index'))

# Закрытие соединения с базой данных
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route('/logout', methods=['POST'])
def logout():
    # Очищаем сессионные данные пользователя
    session.clear()
    # Возвращаем пользователя на стартовую страницу
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Извлечение данных из формы
        form_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'middle_name': request.form.get('middle_name', ''),
            'email': request.form['email'],
            'phone_number': request.form.get('phone_number', ''),
            'institution': request.form.get('institution', ''),
            'position': request.form.get('position', ''),
            'subjects_taught': request.form.get('subjects_taught', ''),
            'academic_degree': request.form.get('academic_degree', ''),
            'academic_rank': request.form.get('academic_rank', '')
        }

        # Проверка уникальности Email
        db = get_db()
        existing_email = db.execute("SELECT COUNT(*) FROM users WHERE email=:email", {'email': form_data['email']}).fetchone()[0]
        if existing_email > 0:
            flash("Такой email уже существует")
            return redirect(url_for('register'))

        # Вставка новых данных
        cur = db.cursor()
        cur.execute(
            '''INSERT INTO users (first_name, last_name, middle_name, email, phone_number, institution, position, subjects_taught, academic_degree, academic_rank)
               VALUES (:first_name, :last_name, :middle_name, :email, :phone_number, :institution, :position, :subjects_taught, :academic_degree, :academic_rank)''',
            form_data
        )
        db.commit()

        flash("Заявка успешно отправлена")
        return redirect(url_for('index'))

    return render_template('index.html')


# Страница администратора
@app.route('/admin')
def admin_page():
    return render_template('ADMINSISTEM/Admin.html')

@app.route('/ixpertiza')
def ixpertiza_page():
    return render_template('ixpertiza/ixpertiza.html')

@app.route('/ixpertiza2')
def ixpertiza2_page():
    return render_template('ixpertiza/ixpertiza2.html')

@app.route('/konstruktor0')
def konstruktor0_page():
    return render_template('konstruktor/konstruktor0.html')


@app.route('/konstruktor2')
def konstruktor2_page():
    return render_template('konstruktor/konstruktor2.html')

@app.route('/konstruktor3')
def konstruktor3_page():
    return render_template('konstruktor/konstruktor3.html')

@app.route('/get_authors', methods=['GET'])
def get_authors():
    db = get_db()
    authors = db.execute(
        "SELECT user_id, first_name, last_name, institution, position "
        "FROM users WHERE role_author = TRUE"
    )
    result = []
    for author in authors.fetchall():
        result.append({
            "value": f"{author['first_name']} {author['last_name']}",
            "data": {
                "institution": author['institution'],
                "position": author['position']
            }
        })
    return jsonify(result)

@app.route('/save_authors', methods=['POST'])
def save_authors():
    data = request.get_json()
    first_coauthor = data.get('first_coauthor')
    second_coauthor = data.get('second_coauthor')

    # Можно сохранить данные в базу данных или временно в сессии
    session['coauthors'] = {
        'first': first_coauthor,
        'second': second_coauthor
    }

    return jsonify(success=True)

@app.route('/konstruktor4')
def konstruktor4_page():
    return render_template('konstruktor/konstruktor4.html')

@app.route('/konstruktor5')
def konstruktor5_page():
    return render_template('konstruktor/konstruktor5.html')

@app.route('/konstruktor6')
def konstruktor6_page():
    return render_template('konstruktor/konstruktor6.html')

@app.route('/konstruktor7')
def konstruktor7_page():
    return render_template('konstruktor/konstruktor7.html')

@app.route('/konstruktor8')
def konstruktor8_page():
    return render_template('konstruktor/konstruktor8.html')

@app.route('/konstruktor9')
def konstruktor9_page():
    return render_template('konstruktor/konstruktor9.html')

@app.route('/smenit-experta')
def smenit_experta():
    return render_template('ADMINSISTEM/smenit-ixperta.html')

@app.route('/DPP_PK')
def DPP_PK():
    return render_template('ADMINSISTEM/DPP-PK.html')

@app.route('/rekomendacii')
def rekomendacii():
    return render_template('ADMINSISTEM/rekomendacii.html')

@app.route('/show-candidates')
def show_candidates():
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Выборка всех пользователей из базы данных
        cursor.execute('''
            SELECT first_name, last_name, middle_name, email, phone_number, institution, position, subjects_taught, academic_degree, academic_rank 
            FROM users 
            WHERE role_admin=FALSE AND role_author=FALSE AND role_expert=FALSE
        ''')
        results = cursor.fetchall()
        
    
        print("Полученные данные:", results)

         # Нормализация данных и замена пустых значений на "не указано"
        candidates = []
        for result in results:
            # Устанавливаем разумные значения по умолчанию
            default_values = ['не указано'] * 10
            processed_result = list(result[:len(default_values)])
            for i in range(len(processed_result)):
                if processed_result[i] is None:
                    processed_result[i] = default_values[i]

            # Создаем полноценный объект кандидата
            candidates.append({
                'full_name': f"{processed_result[0]} {processed_result[1]} {processed_result[2]}",
                'email': processed_result[3],
                'phone_number': processed_result[4],
                'institution': processed_result[5],
                'position': processed_result[6],
                'subjects_taught': processed_result[7],
                'academic_degree': processed_result[8],
                'academic_rank': processed_result[9]
            })# Конвертирование результатов в удобный формат
            
        
        return render_template('ADMINSISTEM/knopka-kandidati.html', candidates=candidates)
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Ошибка загрузки данных"

def send_declination_email(email_address):
    sender_email = "kirilll.nikitin2017@mail.ru"   # ВАЖНО! Укажите свою реальную почту
    receiver_email = email_address                 # Адрес получателя (он приходит из запроса)
    subject = "Отказ в вашей заявке"
    message_body = """\
    Уважаемый кандидат!

    К сожалению, Ваша заявка была отклонена. Спасибо за Ваше участие.

    С уважением,
    Команда нашего сайта
    """

    # Формирование письма
    msg = EmailMessage()
    msg.set_content(message_body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Отправка письма через Mail.ru с SSL/TLS
    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
        server.login(sender_email, "FR6K9bicQTqds6soRfcG")  # ВАЖНО! Используйте реальный пароль своей почты
        server.send_message(msg)

    print(f"Сообщение отправлено на {receiver_email}.")

@app.route('/send-decline-email', methods=['POST'])
def send_decline_email_route():
    data = request.get_json()
    recipient_email = data.get("email")
    
    if recipient_email:
        # Сначала отправляем уведомление кандидату
        send_declination_email(recipient_email)
        
        # Затем получаем соединение с базой данных
        db = get_db()
        
        # Удаляем запись кандидата из базы данных по email
        db.execute(
            "DELETE FROM users WHERE email=?",
            (recipient_email,)
        )
        db.commit()
        
        return jsonify({"message": "Кандидат уведомлён и удалён из базы."})
    else:
        return jsonify({"error": "Адрес электронной почты отсутствует"}), 400
    
def send_acceptance_email(email_address):
    sender_email = "kirilll.nikitin2017@mail.ru"   # ВАЖНО! Укажите свою реальную почту
    receiver_email = email_address                 # Адрес получателя (он приходит из запроса)
    subject = "Поздравляем! Вы приняты!"
    message_body = """
    Уважаемый кандидат!
    
    Мы рады сообщить Вам, что Ваша заявка одобрена и теперь Вы являетесь автором нашей платформы.
    
    С уважением,
    Команда нашего сайта
    """

    # Формирование письма
    msg = EmailMessage()
    msg.set_content(message_body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Отправка письма через Mail.ru с SSL/TLS
    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
        server.login(sender_email, "FR6K9bicQTqds6soRfcG")  # ВАЖНО! Используйте реальный пароль своей почты
        server.send_message(msg)

    print(f"Сообщение отправлено на {receiver_email}.")
    
@app.route('/send-accept-email', methods=['POST'])
def send_accept_email_route():
    data = request.get_json()
    recipient_email = data.get("email")
    
    if recipient_email:
        # Отправляем письмо кандидату о принятии
        send_acceptance_email(recipient_email)
        
        # Обновляем роль кандидата в базе данных
        db = get_db()
        db.execute(
            "UPDATE users SET role_author=TRUE WHERE email=?",
            (recipient_email,)
        )
        db.commit()
        
        return jsonify({"message": "Кандидат принят и получил роль автора"})
    else:
        return jsonify({"error": "Адрес электронной почты отсутствует"}), 400


def send_reset_email(email_address, token):
    sender_email = "kirilll.nikitin2017@mail.ru"  # Используем существующий аккаунт
    receiver_email = email_address  # Получатель — адрес пользователя
    subject = "Сброс пароля на вашем аккаунте"
    message_body = f"""\
    Уважаемый пользователь!

    Вы запросили сброс пароля. Для завершения процедуры сброса пароля перейдите по следующей ссылке:

    {url_for('reset_password', token=token, _external=True)}

    Если вы не запрашивали сброс пароля, просто проигнорируйте данное письмо.

    С уважением,
    Администрация портала
    """

    # Формирование письма
    msg = EmailMessage()
    msg.set_content(message_body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Отправка письма через Mail.ru с SSL/TLS
    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
        server.login(sender_email, "FR6K9bicQTqds6soRfcG")  # Используем пароль от действующего аккаунта
        server.send_message(msg)

    print(f"Сообщение отправлено на {receiver_email}.")

def generate_reset_token():
    token = secrets.token_hex(32)  # Генерируем случайный токен
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Срок действия токена — 1 час
    return token, expires_at

def update_user_password(user_id, new_password):
    # Получаем соединение с базой данных
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET password=? WHERE id=?", (generate_password_hash(new_password), user_id))
    db.commit()

@app.route('/request-reset', methods=['POST'])
def request_reset():
    email = request.form.get('email')
    # Проверяем наличие пользователя с данным email
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email=?", (email,))  # Используем правильный идентификатор пользователя
    user = cursor.fetchone()

    if user:
        # Генерируем токен и отправляем письмо
        token, _ = generate_reset_token()
        send_reset_email(email, token)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "Пользователь с указанным email не зарегистрирован."}), 400


@app.route('/edit-profile', methods=['POST'])
def edit_profile():
    user_id = request.form.get('user_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    # Обновляем данные пользователя
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET first_name=?, last_name=?, email=? WHERE id=?", (first_name, last_name, email, user_id))
    db.commit()
    return "Профиль успешно обновлён."


@app.route('/reset-password/<string:token>', methods=['GET'])
def reset_password(token):
    # Здесь логика проверки валидности токена и отображения страницы смены пароля
    return render_template('reset_password.html')

# СТРАНИЦА ПОЛЬЗОВАТЕЛИ
@app.route('/polzovateli')
def polzovateli():
    db = get_db()
    cursor = db.execute('''
        SELECT 
            u.user_id,            
            u.first_name,
            u.middle_name,
            u.last_name,
            u.institution,
            u.position,
            u.academic_degree,
            u.email,                     
            u.phone_number,            
            u.username,                 
            u.password,             
            (
                SELECT GROUP_CONCAT(role_text, '<br />')
                FROM (
                    SELECT 'Администратор' AS role_text WHERE u.role_admin = TRUE UNION ALL
                    SELECT 'Автор' AS role_text WHERE u.role_author = TRUE UNION ALL
                    SELECT 'Эксперт' AS role_text WHERE u.role_expert = TRUE
                )
            ) AS roles
        FROM users u
        WHERE u.role_admin OR u.role_author OR u.role_expert
    ''')
    
    users = []
    for row in cursor.fetchall():
        user = dict(row)
        # Преобразуем строку ролей в массив
        user['roles'] = user['roles'].split('<br />')
        users.append(user)
    
    return render_template('ADMINSISTEM/knopka-polzovateli.html', users=users)

@app.route('/archive')
def archive():
    return render_template('ADMINSISTEM/archive.html')


@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    print("Received Data:", data)  # Логируем полученные данные

    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'user_id отсутствует'}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    institution = data.get('institution')
    position = data.get('position')
    academic_degree = data.get('academic_degree')

    # Роли разбиваем на булевые признаки
    role_admin = 'Администратор' in data.get('roles', [])
    role_author = 'Автор' in data.get('roles', [])
    role_expert = 'Эксперт' in data.get('roles', [])

    db = get_db()
    cursor = db.cursor()

    # Проверим существование записи с указанным user_id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        print("No such user found with this user_id:", user_id)
        return jsonify({'status': 'error', 'message': 'Пользователь не найден'}), 404

    # Обновляем данные пользователя, включая роли
    cursor.execute('''
        UPDATE users
        SET first_name=?, last_name=?, email=?, phone_number=?,
            institution=?, position=?, academic_degree=?,
            role_admin=?, role_author=?, role_expert=?
        WHERE user_id=?
    ''', (
        first_name, last_name, email, phone_number, institution,
        position, academic_degree,
        role_admin, role_author, role_expert, user_id
    ))

    db.commit()

    return jsonify({'status': 'ok'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    db.commit()
    return jsonify({'status': 'ok'})

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    institution = data.get('institution')
    position = data.get('position')
    academic_degree = data.get('academic_degree')
    roles = data.get('roles', [])

    # Подготавливаем запрос на вставку
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO users (
            username, password, first_name, last_name, email, phone_number, institution, position, academic_degree
        ) VALUES (?,?,?,?,?,?,?,?,?)
    ''', (username, password, first_name, last_name, email, phone_number, institution, position, academic_degree))

    # Установим роли отдельно
    for role in roles:
        if role == 'Администратор':
            cursor.execute("UPDATE users SET role_admin=TRUE WHERE username=?", (username,))
        elif role == 'Автор':
            cursor.execute("UPDATE users SET role_author=TRUE WHERE username=?", (username,))
        elif role == 'Эксперт':
            cursor.execute("UPDATE users SET role_expert=TRUE WHERE username=?", (username,))

    db.commit()
    return jsonify({'status': 'ok'})

# СПРАВОЧНИКИ
@app.route('/spravochniki')
def spravochniki():
    return render_template('ADMINSISTEM/spravochniki.html')

@app.route('/api/institutions')
def get_institutions():
    db = get_db()
    cursor = db.execute('SELECT institution_id, short_name, full_name FROM institutions')
    institutions = [{
        'institution_id': inst['institution_id'],
        'short_name': inst['short_name'],
        'full_name': inst['full_name']
    } for inst in cursor.fetchall()]
    return jsonify(institutions)

@app.route('/save-institution', methods=["PUT"])
def saveInstitution():
    data = request.json
    short_name = data.get('short_name')
    full_name = data.get('full_name')
    institution_id = data.get('institution_id')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE institutions SET short_name=?, full_name=? WHERE institution_id=?",
        (short_name, full_name, institution_id)
    )
    db.commit()
    return jsonify({'status': 'OK'})

@app.route('/create-institution', methods=["POST"])
def createInstitution():
    data = request.json
    short_name = data.get('short_name')
    full_name = data.get('full_name')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO institutions (short_name, full_name) VALUES (?, ?)",
        (short_name, full_name)
    )
    db.commit()
    return jsonify({'status': 'OK'})

# Маршрут для получения всех учреждений из БД
@app.route('/api/get_all_institutions', methods=['GET'])  # Изменили имя пути
def get_all_institutions():                             # Изменили имя функции
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM institutions")
    rows = cursor.fetchall()
    institutions = []
    for row in rows:
        institutions.append({
            'institution_id': row[0],
            'short_name': row[1],
            'full_name': row[2]
        })
    return jsonify(institutions)

@app.route('/tpud')
def tpud_page():
    return render_template('ADMINSISTEM/tpud.html')


@app.route('/labor/functions', methods=['GET'])
def get_labor_functions():
    """
    Возвращает список всех трудовых функций.
    """
    db = get_db()
    functions = db.execute(
        'SELECT * FROM labor_functions'
    ).fetchall()
    return jsonify([dict(f) for f in functions])



@app.route('/labor/actions/<int:function_id>', methods=['GET'])
def get_labor_actions(function_id):
    """
    Возвращает список действий для указанной трудовой функции.
    """
    db = get_db()
    actions = db.execute(
        'SELECT * FROM labor_actions WHERE function_id = ?', (function_id,)
    ).fetchall()
    return jsonify([dict(a) for a in actions])

@app.route('/labor/add_function', methods=['POST'])
def add_labor_function():
    """
    Добавляет новую трудовую функцию.
    """
    data = request.get_json()
    function_name = data.get('function_name')
    if not function_name:
        return jsonify({'error': 'Название функции обязательно'}), 400

    db = get_db()
    db.execute(
        'INSERT INTO labor_functions (function_name) VALUES (?)', (function_name,)
    )
    db.commit()
    return jsonify({'status': 'ok'})

@app.route('/labor/add_action', methods=['POST'])
def add_labor_action():
    data = request.get_json()
    action_name = data.get('action_name')
    function_id_str = data.get('function_id')

    if not action_name or not function_id_str or not function_id_str.isdigit():
        return jsonify({'error': 'Необходимо указать название действия и верный id функции'}), 400

    function_id = int(function_id_str)

    db = get_db()
    db.execute(
        'INSERT INTO labor_actions (action_name, function_id) VALUES (?, ?)', (action_name, function_id)
    )
    db.commit()
    return jsonify({'status': 'ok'})

@app.route('/labor/actions/bulk', methods=['POST'])
def bulk_get_actions():
    """
    Возвращает список действий для нескольких функций одновременно.
    """
    data = request.get_json()
    function_ids = data.get('function_ids')

    if not function_ids:
        return jsonify([]), 400

    db = get_db()
    actions = db.execute(
        'SELECT * FROM labor_actions WHERE function_id IN ({ids})'.format(ids=", ".join(map(str, function_ids)))
    )

    return jsonify([dict(a) for a in actions])






@app.route('/obazanosti')
def obazanosti_page():
    return render_template('ADMINSISTEM/obazanosti.html')

@app.route('/get-duties', methods=['GET'])
def get_duties():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM duties;")
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append({"id": row[0], "responsibility": row[1]})
    conn.close()
    return jsonify(results)

@app.route('/add-duty', methods=['POST'])
def add_duty():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO duties (responsibilities) VALUES (?);", (data['responsibility'], ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Обязанность добавлена.'}), 201

@app.route('/remove-duty/<int:duty_id>', methods=['DELETE'])
def remove_duty(duty_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM duties WHERE id=?;", (duty_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Обязанность удалена.'}), 200

@app.route('/api/duties')
def fetch_duties():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT responsibilities FROM duties")
    results = cur.fetchall()
    return jsonify([{'responsibilities': r[0]} for r in results])


@app.route('/categories')
def categories_page():
    return render_template('ADMINSISTEM/categories.html')

@app.route('/get-listener-categories', methods=['GET'])
def get_listener_categories():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM listener_categories;")
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append({"category_id": row[0], "category_name": row[1]})
    conn.close()
    return jsonify(results)

@app.route('/add-listener-category', methods=['POST'])
def add_listener_category():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO listener_categories (category_name) VALUES (?);", (data['category_name'], ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Категория добавлена.'}), 201

@app.route('/remove-listener-category/<int:category_id>', methods=['DELETE'])
def remove_listener_category(category_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM listener_categories WHERE category_id=?;", (category_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Категория удалена.'}), 200

@app.route('/get-listener-categories', endpoint='get_listener_categories_api', methods=['GET'])
def get_listener_categories():
    db = get_db()
    cursor = db.execute('SELECT * FROM listener_categories')
    categories = []
    for cat in cursor.fetchall():
        categories.append({
            'category_id': cat['category_id'],
            'category_name': cat['category_name']
        })
    return jsonify(categories)

@app.route('/education')
def education_page():
    return render_template('ADMINSISTEM/education.html')

@app.route('/get-education-forms', methods=['GET'])
def get_education_forms():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM education_forms;")
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append({"form_id": row[0], "form_name": row[1]})
    conn.close()
    return jsonify(results)

@app.route('/add-education-form', methods=['POST'])
def add_education_form():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO education_forms (form_name) VALUES (?);", (data['form_name'], ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Форма обучения добавлена.'}), 201

@app.route('/remove-education-form/<int:form_id>', methods=['DELETE'])
def remove_education_form(form_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM education_forms WHERE form_id=?;", (form_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Форма обучения удалена.'}), 200

if __name__ == '__main__':
    app.run(debug=True)

