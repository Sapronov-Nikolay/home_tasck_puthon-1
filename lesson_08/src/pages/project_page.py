# src/pages/project_page.py
# PageObject для проектов YouGile.
# Инкапсулирует HTTP-запросы и формирование payload, оставляя тесты чистыми.

from ..api_client import YouGileApiClient

class ProjectPage:
    """
    Страница (PageObject) для проектов.
    Отвечает за бизнес-логику операций над проектами: создание, чтение, обновление, удаление.
    Не знает про авторизацию и сеть — эту ответственность делегирует YouGileApiClient.
    Такой подход упрощает тестирование.
    """

    def __init__(self, client=None):
        """
        Инициализация страницы.
        client: экземпляр YouGileApiClient (для тестов можно передать имитацию - мок).
        Если client не передан — создаём реальный клиент.
        Это позволяет писать тесты без реального API (через имитацию - мок) и при этом иметь рабочий код.
        """
        self.client = client if client else YouGileApiClient()

    def create(self, title, users=None):
        """
        Создать проект.
        title: обязательное поле (имя проекта).
        users: необязательный список ID пользователей для назначения в проект.

        Примечание: поле users добавляется только если оно явно передано.
        Это сделано для того, чтобы не отправлять пустой список или null,
        так как API YouGile может некорректно обработать такие значения
        (это особенность API, замеченная при тестировании).
        :return: Response объект (ответ API)
        """
        payload = {"title": title}
        if users:
            payload["users"] = users
        return self.client.post("/api-v2/projects", payload)

    def get(self, project_id):
        """
        Получить данные проекта по его ID.
        Используем GET-запрос к /api-v2/projects/{project_id}.
        Возвращает ответ requests (можно проверить status_code и resp.json()).
        """
        return self.client.get(f"/api-v2/projects/{project_id}")

    def update(self, project_id, title=None, deleted=None):
        """
        Обновить проект.
        Поддерживаем только title и deleted — это те поля, которые реально можно менять через API.

        Почему не добавляем description:
            - Из курсовой по тестированию YouGile известно, что добавление description (не поддерживается)
            - Если API не поддерживает обновление description для проектов error = 400 — не стоит слать лишнее.
            - Лишние поля могут привести к ошибке валидации или непредсказуемому поведению.

        Логика payload:
            - Добавляем поля только если они явно переданы (None означает «не трогаем это поле»).
            - Такой подход позволяет обновлять только нужные поля (частичное обновление).
        """
        payload = {}
        if title is not None:
            payload["title"] = title
        if deleted is not None:
            payload["deleted"] = deleted
        return self.client.put(f"/api-v2/projects/{project_id}", payload)

    def delete(self, project_id):
        """
        Удалить проект.
        В YouGile это «мягкое удаление» (soft delete) — проект скрывается, но не стирается навсегда.
        Реализуем через вызов update(..., deleted=True), чтобы не дублировать логику запроса.
        Такой подход делает код DRY (Don't Repeat Yourself) и уменьшает риск рассинхронизации.
        """
        return self.update(project_id, deleted=True)
