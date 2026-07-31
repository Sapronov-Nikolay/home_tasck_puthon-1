# conftest.py
# Фикстуры для pytest. Добавляют src/ в путь и создают тестовые проекты.

import sys
from pathlib import Path

# Добавляем папку src/ в sys.path, чтобы импорты работали
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest
from src.pages.project_page import ProjectPage

@pytest.fixture(scope='session')
def project_page():
    """Один экземпляр ProjectPage на всю сессию тестирования."""
    return ProjectPage()

@pytest.fixture
def temp_project(project_page):
    """
        Фикстура создаёт проект с уникальным названием перед тестом,
        а после теста скрывает его (deleted: true), так как API YouGile. Возвращает ID проекта
        не поддерживает физическое удаление проектов.
    """
    import time
    # Решили использовать Faker для генерации имён (названий)
    try:
        from faker import Faker
        faker = Faker()
        title = f"Проект {faker.word()}"
    except ImportError:
        title = f"AutoTest_{int(time.time())}"

    resp = project_page.create(title)
    assert resp.status_code == 201, "Не удалось создать проект"
    project_id = resp.json()["id"]
    yield project_id
    # Очистка после теста
    project_page.delete(project_id)
