# tests/test_projects.py
# Позитивные и негативные тесты для проектов YouGile.
# Используют PageObject и фикстуры из conftest.py.

import requests


# ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------
# Проверяют корректную работу API: ожидаем успех (2xx), наличие нужных полей, правильное поведение.

def test_create_project_positive(project_page):
    """
        Создаём проект - ожидается статус 201 и наличие id в ответе.
        Это базовый позитивный сценарий: проект создаётся, API возвращает данные.
        Очистка: сразу скрываем проект (soft delete), чтобы не засорять тестовую организацию.
        Так тест остаётся идемпотентный - то есть неизменный: его можно запускать много раз без накопления мусора.
    """
    title = "Позитивный проект"
    resp = project_page.create(title)
    assert resp.status_code == 201, f"Ожидался статус 201, но получен {resp.status_code}"
    data = resp.json()
    assert "id" in data, "В ответе должен быть id проекта"

    # Очистка: скрываем проект, чтобы не плодить тестовые сущности. но потом надо будет ручками почистить в UI
    project_page.delete(data["id"])

def test_get_project_positive(project_page, temp_project):
    """
        Получение проекта по ID - ожидаем 200, совпадение id и наличие title. Смотрим что создали
        temp_project - фикстура для автоматической генерации имён, заранее создаёт проект и возвращает его id.
        Тест проверяет, что GET-запрос корректно возвращает данные созданного проекта.
    """
    project_id = temp_project
    resp = project_page.get(project_id)
    assert resp.status_code == 200, f"Ожидается статус 200, но получен {resp.status_code}"
    data = resp.json()
    assert data["id"] == project_id, f"ID в ответе должен совпадать с запрошенным"
    assert "title" in data, "В ответе должно быть поле title"

def test_update_project_positive(project_page, temp_project):
    """
        Обновление названия проекта - ожидаем статус 200 и возвращение через GET.
        Проверяем не только статус ответа PUT, но и реальное изменение данных через отдельный GET.
        Это защищает от ситуации, когда API выдаёт код 200, но ничего не меняет, но суде по прогонам в postman всё ОК
    """
    project_id = temp_project
    new_title = "Обновлён позитивный проект"
    resp = project_page.update(project_id, title=new_title)
    assert resp.status_code == 200, f"Ожидался статус 200, но получен {resp.status_code}"
    # Убеждаемся что название действительно изменилось.
    get_resp = project_page.get(project_id)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == new_title, "Название проекта должно совпадать с новым значением"

def test_delete_project_positive(project_page, temp_project):
    """
        Мягкое удаление (сокрытие) проекта - ожидаем 200 и deleted: true при GET.
        В интерфейсе проект не удалится, а будет скрыт и помечен как deleted.
        Тест подтверждает, что флаг deleted корректно устанавливается и виден при получении данных.
    """
    project_id = temp_project
    resp = project_page.delete(project_id)
    assert resp.status_code == 200, f"Ожидался ответ 200, но получен {resp.status_code}"
    # Проверяем, что проект действительно помечен как удалённый.
    get_resp = project_page.get(project_id)
    assert get_resp.status_code == 200
    assert get_resp.json().get("deleted") is True, "Поле deleted должно быть True после удаления"

# ---------- НЕГАТИВНЫЕ ТЕСТЫ ----------
# Проверяют обработку ошибок: неверные данные, несуществующие ID, неподдерживаемые поля.
# Здесь мы намеренно вызываем ошибки API и проверяем, что система ведёт себя предсказуемо.

def test_create_project_empty_title(project_page):
    """
        Пытаемся создать проект с пустым названием - ожидаем 400.
        API должен отключить запрос, потому что title - обязательное поле. Тут мы как бы пишем в названии ничего.
        Проверяем и статус, и наличие сообщения об ошибке в ответе.
    """
    resp = project_page.create("")
    assert resp.status_code == 400, f"Ожидался статус 400, но получен {resp.status_code}"
    # message упрощает понимание ошибок, проверяем, что API вернул объяснение ошибки.
    assert "message" in resp.json(), "В ответе должна быть информация об ошибке"


def test_get_project_not_found(project_page):
    """
    Получение несуществующего проекта – ожидаем 404.
    Используем заведомо неверный UUID (все нули) — такой проект точно не существует.
    Тест гарантирует, что API корректно сообщает об отсутствии ресурса.
    """
    fake_id = "00000000-0000-0000-0000-000000000000"
    resp = project_page.get(fake_id)
    assert resp.status_code == 404, f"Ожидался статус 404, но получен {resp.status_code}"


def test_update_project_not_found(project_page):
    """
    Обновление несуществующего проекта – ожидаем 404.
    Аналогично предыдущему тесту: используем несуществующий ID.
    Убеждаемся, что PUT-запрос тоже корректно возвращает 404 при отсутствии ресурса.
    """
    fake_id = "00000000-0000-0000-0000-000000000000"
    resp = project_page.update(fake_id, title="Новое название")
    assert resp.status_code == 404, f"Ожидался статус 404, но получен {resp.status_code}"


def test_update_project_with_description(project_page, temp_project):
    """
    Пытаемся обновить проект с полем description, не поддерживающимся в API).
    Ожидаем 400 и сообщение об ошибке, связанное с description.

    Тест написан через прямой requests, а не через ProjectPage:
      - ProjectPage сознательно не поддерживает description (чтобы не слать лишние поля).
      - Намеренно обходим абстракцию, чтобы протестировать поведение API при лишнем поле.
      - Это тест: проверяем, что API не позволяет указывать неподдерживаемые данные.
    """
    project_id = temp_project
    client = project_page.client
    url = f"{client.base_url}/api-v2/projects/{project_id}"
    payload = {"title": "Название", "description": "Описание"}
    headers = client._headers()
    resp = requests.put(url, json=payload, headers=headers)
    assert resp.status_code == 400, f"Ожидался статус 400, но получен {resp.status_code}"
    # Читаем объяснение от сервака
    error_data = resp.json().get("message")
    if isinstance(error_data, list):
        error_msg = " ".join(error_data)
    else:
        error_msg = str(error_data)
    assert "description" in error_msg.lower(), "Сообщение об ошибке должно упоминать description"
