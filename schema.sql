-- Таблица Пользователи (Users)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор пользователя (первичный ключ)
    username VARCHAR(50) UNIQUE, -- уникальное имя пользователя (никнейм)
    password_hash VARCHAR(100), -- хэшированный пароль пользователя
    role_admin BOOLEAN DEFAULT FALSE, -- признак роли администратора (false по умолчанию)
    role_author BOOLEAN DEFAULT FALSE, -- признак роли автора (false по умолчанию)
    role_expert BOOLEAN DEFAULT FALSE, -- признак роли эксперта (false по умолчанию)
    first_name VARCHAR(50), -- имя пользователя
    last_name VARCHAR(50), -- фамилия пользователя
    middle_name VARCHAR(50), -- отчество пользователя
    email VARCHAR(100) UNIQUE NOT NULL, -- уникальный email пользователя
    phone_number VARCHAR(20) UNIQUE, -- уникальный номер телефона пользователя
    institution VARCHAR(100), -- учреждение, в котором работает пользователь
    position VARCHAR(100), -- должность пользователя
    subjects_taught TEXT, -- преподаваемые дисциплины (нормализованное решение предпочтительнее)
    academic_degree VARCHAR(100), -- академическая степень пользователя
	academic_rank VARCHAR(100) -- академическое звание пользователя
);


-- Таблица учреждений
CREATE TABLE institutions (
    institution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_name VARCHAR(50),
    full_name VARCHAR(100)
);

-- Таблица Reset Tokens
CREATE TABLE reset_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

-- Таблица трудовых функций
CREATE TABLE labor_functions (
    function_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор функции
    function_name VARCHAR(100) NOT NULL -- название функции
);

-- Таблица трудовых действий
CREATE TABLE labor_actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор действия
    action_name VARCHAR(100) NOT NULL, -- название действия
    function_id INTEGER REFERENCES labor_functions(function_id) ON DELETE CASCADE -- внешний ключ, обеспечивающий связь с функцией
);

-- Таблица Должностные Обязанности (Duties)
CREATE TABLE duties (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор
    responsibilities TEXT NOT NULL              -- описание должностных обязанностей
);

-- Таблица Категории слушателей (ListenerCategories)
CREATE TABLE listener_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор категории
    category_name VARCHAR(100) NOT NULL               -- название категории слушателей
);

-- Таблица Формы обучения (EducationForms)
CREATE TABLE education_forms (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор формы обучения
    form_name VARCHAR(100) NOT NULL           -- название формы обучения
);

-- Таблица Программ (Programs)
CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор программы
    title VARCHAR(100) NOT NULL,                 -- Название программы
    current_version INTEGER DEFAULT 1,           -- Текущая версия программы
    status VARCHAR CHECK(status IN ('В разработке', 'На экспертизе', 'Опубликована', 'Отклонена')), -- Статус программы
    main_author_id INTEGER REFERENCES users(user_id), -- Главный автор программы
    coauthor_1_id INTEGER REFERENCES users(user_id), -- Первый соавтор
    coauthor_2_id INTEGER REFERENCES users(user_id), -- Второй соавтор
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата создания программы
    sent_to_expertise_at TIMESTAMP                -- Дата отправки на экспертизу
);

-- Таблица Страниц Программы (ProgramPages)
CREATE TABLE program_pages (
    page_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    page_order INTEGER NOT NULL,                    -- Порядковый номер страницы (например, от 1 до 9)
    content TEXT                                    -- HTML-контент страницы (используем TEXT)
);