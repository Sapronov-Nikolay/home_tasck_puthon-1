import pytest

from db_utils import add_student, get_student_by_id, update_student_age, delete_student, get_all_students


@pytest.fixture
def created_student():
    """
        Фикстура: создаёт одного студента, отдаёт его ID тесту, а после теста удаляет.
        Это решает проблему «мусора» в базе: каждый тест стартует с чистого листа.
        """
    name = "Test Student"
    age = 25
    # 1. Создаём студента в БД.
    add_student(name, age)
    # 2. Получаем всех студентов, чтобы найти ID только что созданного.
    students = get_all_students()
    student = next(s for s in students if s['name'] == name)
    student_id = student['id']
    # 3. yield — ключевое слово pytest для фикстур.
    # Оно означает: «отдай student_id тестам, которые используют эту фикстуру,
    # а всё, что ниже yield, выполни ПОСЛЕ того, как тесты закончатся».
    yield student_id
    # 4. Очистка: удаляем студента после завершения теста.
    delete_student(student_id)

def test_add_student(created_student):
    """
        Проверяем, что студент действительно добавляется и его можно получить по ID.
        created_student — это ID, который вернула фикстура.
    """
    student = get_student_by_id(created_student)
    assert student is not None    # Студент должен быть
    assert student["name"] == "Test Student"    # Имя должно совпадать

def test_update_student(created_student):
    """
        проверяем обновление возраста.
        created_student снова даёт нам ID студента, созданного фикстурой.
    """
    new_age = 30
    update_student_age(created_student, new_age)
    updated = get_student_by_id(created_student)
    assert updated['age'] == new_age    # проверяем, что возраст соответствует обновлённому

def test_delete_student():
    """
        Тест на удаление. Здесь мы НЕ используем created_student. Почему?
        Потому что логика удаления должна быть самостоятельной:
        создали → удалили → проверили, что уделили.
        Если использовать created_student, то удаление произошло бы фикстурой (yield),
        и тест бы не проверил удаление, а только смотрел на уже удалённое.
    """
    name = "To Delete Student"
    add_student(name, 20)   # 1. Создаём, чтобы было что тестировать
    students = get_all_students()
    # Снова находим ID через next(...), как в фикстуре.
    student = next(s for s in students if s["name"] == name)
    student_id = student["id"]  # 2. Находим ID только что созданного
    delete_student(student_id)  # 3. Теперь удаляем то что создали
    deleted = get_student_by_id(student_id)     # 4. Сохраняем проверку факта удаления объекта
    assert deleted is None  # 5. Проверяем, что теперь его нет