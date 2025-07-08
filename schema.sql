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
--CREATE TABLE reset_tokens (
  --  id INTEGER PRIMARY KEY AUTOINCREMENT,
  --  user_id INTEGER REFERENCES users(id),
  --  token TEXT UNIQUE NOT NULL,
  --  expires_at TIMESTAMP NOT NULL
--);

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
    duties_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный идентификатор
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

-- Таблица статусы  (ProgramPages)
CREATE TABLE Status (
    Status_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор статуса
    Status_name VARCHAR(100) NOT NULL   -- название статуса

);

-- Таблица Программ (Programs)
CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор программы
    current_version INTEGER DEFAULT 1,           -- Текущая версия программы
    status_id INTEGER REFERENCES Status(Status_id),
    main_author_id INTEGER REFERENCES users(user_id), -- Главный автор программы
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата создания программы
    sent_to_expertise_at TIMESTAMP                -- Дата отправки на экспертизу
);

-- Таблица Страниц Программы (ProgramPages)
CREATE TABLE program_pages2 (
    page2_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    program_name VARCHAR(100) NOT NULL,  -- название программы
    institution_ID INTEGER REFERENCES institutions(institution_id),
    institution_new  VARCHAR(100)
);

-- Таблица Страницы3 Программы (ProgramPages)
CREATE TABLE program_pages3 (
    page3_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    coauthor_1_id INTEGER REFERENCES users(user_id), -- Первый соавтор
    coauthor_2_id INTEGER REFERENCES users(user_id) -- Второй соавтор
);

CREATE TABLE program_pages4 (
    page4_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    Abbreviation VARCHAR(100) NOT NULL,
    Full_name VARCHAR(100) NOT NULL-- название программы
);

CREATE TABLE Prof_standard (
    Prof_standard_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    Prof_standard_name VARCHAR(100) NOT NULL-- название проф. стандарта (ЕКС и тп)

);

CREATE TABLE program_pages5 (
    page5_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    relevance TEXT, -- Актуальность разработки программы
    goal TEXT, -- Цель реализации программы
    prof_standard_id INTEGER REFERENCES Prof_standard(Prof_standard_id), -- проф. стандарт_ID (внешний ключ)
    job_responsibilities_id INTEGER REFERENCES duties(duties_id), -- Должностные обязанности_ID (внешний ключ)
    new_job_responsibilities TEXT, -- Должностные обязанности_новые
    knowledge_required TEXT, -- Знать
    skills_required TEXT, -- Уметь
    listener_category_id INTEGER REFERENCES listener_categories(category_id), -- Категория слушателей_id (внешний ключ)
    education_form_id INTEGER REFERENCES education_forms(form_id), -- Форма обучения_id (внешний ключ)
    duration_hours INTEGER -- Срок освоения (часы)
);

CREATE TABLE Moduli_educat (
    Moduli_educat_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    Moduli_educat_name VARCHAR(100) NOT NULL
);

CREATE TABLE Attestat (
    Attestat_ID INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    Attestat_name VARCHAR(100) NOT NULL
);

CREATE TABLE program_pages7 (
    page7_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    Moduli_id INTEGER  REFERENCES Moduli_educat(Moduli_educat_id),  -- ссылка на таблицу modules (id модуля)
    Theme TEXT NOT NULL,                   -- тема модуля
    Total_Hours INTEGER,                   -- общее количество часов
    Practical_Hours INTEGER,               -- количество часов практических занятий
    Distance_Learning BOOLEAN DEFAULT FALSE     -- дистанционное обучение (true/false)

);

CREATE TABLE program_pages8 (
    page8_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
    Attestats_id INTEGER REFERENCES Attestat(Attestat_ID),  -- Аттестационный идентификатор
    Requirements_Description TEXT,                  -- Описание требований
    Topic TEXT,                                     -- Тема
    Hours_Count INTEGER,                            -- Количество часов
    Evaluation_Criteria TEXT,                       -- Критерии оценки
    Task_Examples TEXT,                             -- Примеры заданий
    Attempt_Count INTEGER                           -- Количество попыток
);

CREATE TABLE program_pages9 (
    page9_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Уникальный идентификатор страницы
    program_id INTEGER REFERENCES programs(program_id), -- Идентификатор программы
 Normative_Documents TEXT, -- нормативные документы
    Main_Literature TEXT, -- основная литература
    Additional_Literature TEXT, -- дополнительная литература
    Electronic_Educational_Materials TEXT, -- электронные учебные материалы
    Internet_Resources TEXT, -- интернет-ресурсы
    Computer BOOLEAN DEFAULT FALSE, -- наличие компьютера (Да/Нет)
    Projector BOOLEAN DEFAULT FALSE, -- наличие проектора (Да/Нет)
    Interactive BOOLEAN DEFAULT FALSE, -- интерактивное оборудование (Да/Нет)
    Speakers BOOLEAN DEFAULT FALSE, -- наличие колонок (Да/Нет)
    Whiteboards_or_Flipcharts BOOLEAN DEFAULT FALSE, -- маркерные доски или флипчарты (Да/Нет)
    Other_Auditorium BOOLEAN DEFAULT FALSE, -- другое аудиторное оборудование (Да/Нет)
    Auditorium_Equipment TEXT, -- дополнительное описание оборудования аудитории
    Personal_Computer_with_Internet BOOLEAN DEFAULT FALSE, -- персональный компьютер с доступом в интернет (Да/Нет)
    Speaker_for_Materials BOOLEAN DEFAULT FALSE, -- динамик для воспроизведения учебных материалов (Да/Нет)
    Standard_Software BOOLEAN DEFAULT FALSE, -- стандартное программное обеспечение (Да/Нет)
    Other_Remote BOOLEAN DEFAULT FALSE, -- другое дистанционное оборудование (Да/Нет)
    Remote_Equipment TEXT , -- описание дополнительного дистанционного оборудования
    Personnel_Provision TEXT -- кадровое обеспечение
);

