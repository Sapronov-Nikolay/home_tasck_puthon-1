from sqlalchemy import create_engine, text, inspect

# Формат: postgresql://пользователь:пароль@хост:порт/имя_базы
DB_STRING = "postgresql://postgres:quein@localhost:5432/mydatabase"

# Он не подключается сразу, а хранит настройки: куда стучаться, как переподключиться, сколько держать соединений.
engine = create_engine(DB_STRING)

# Создаём таблицу с колонками для имени и возраста

def create_table_if_not_exists():
    """Создаёт таблицу students, если она не существует."""
    with engine.connect() as connection:
        inspector = inspect(engine)
        if not inspector.has_table("students"):
            try:
                connection.execute(text("""
                    CREATE TABLE students (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        age INTEGER
                    )
                """))
                connection.commit()
                print("✅ Таблица students создана.")
            except Exception as e:
                print(f"❌ ОШИБКА при создании таблицы: {e}")
                raise  # Перебросить исключение, чтобы тест упал и мы увидели
        else:
            print("ℹ️ Таблица students уже существует.")

create_table_if_not_exists()

def add_student(name, age):
    '''Добавляем студента в таблицу students'''
    with engine.connect() as connection:
        connection.execute(
            text("INSERT INTO students (name, age) VALUES (:name, :age)"),
            {'name': name, 'age': age}  # Словарь: подставляем реальные значения вместо :name и :age
        )
        # Без этой строки база данных может всё забыть после закрытия соединения.
        connection.commit()

def get_student_by_id(student_id):
    """Получить одного студента по ID."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM students WHERE id = :id"),
            {"id": student_id}
        )
        # .mappings() - превращает строки базы в удобные словари типа {"id": 1, "name": "...", "age": 25}.
        # Раньше это были кортежи (1, "name", 25) - это не удобно читать.
        # .first() - будет только первую строку (потому что по ID обычно один студент).
        # Если ничего не найдено - вернёт None, а не ошибку.
        return result. mappings().first()


def update_student_age(student_id, new_age):
    """Обновить возраст студента по ID"""
    with engine.connect() as connection:
        connection.execute(
            text("UPDATE students SET age = :age WHERE id = :id"),
            {'age': new_age, 'id': student_id}
        )
        connection.commit()

def delete_student(student_id):
    """Удалить студента по ID."""
    with engine.connect() as connection:
        connection.execute(
            text("DELETE FROM students WHERE id = :id"),
            {"id": student_id}
        )
        connection.commit()


def get_all_students():
    """Получить всех студентов из таблицы."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM students"))
        # .all() — возвращает список всех строк.
        # С .mappings() это будет список словарей: [{"id":1,"name":"..."}, {"id":2,"name":"..."}]
        return result.mappings().all()
