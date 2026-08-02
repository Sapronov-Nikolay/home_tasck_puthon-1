# src/api_client.py
# Клиент для работы с API YouGile.
# Автоматически авторизуется (получает ключ) при первом запросе.

import os, requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env (локальные настройки проекта).
# Это позволяет не хардкодить URL, логин и ключи прямо в коде.
load_dotenv()

class YouGileApiClient:
    """
        Класс-клиент для взаимодействия с Yougile API.
        Главный смысл: не требует ручного токена - делает это сам при первом запросе.
        Также кэширует в памяти, чтобы не запрашивать его на каждый запрос.
    """
    def __init__(self):
        # инициализируем базовые параметры из переменных окружения.
        # Если чего-то нет - будет None, и дальше код должен обработает эту ситуацию.
        self.base_url = os.getenv("YOUGILE_URL")
        self.login = os.getenv("YOUGILE_LOGIN")
        self.password = os.getenv("YOUGILE_PASSWORD")
        self.company_id = os.getenv("YOUGILE_COMPANY_ID")

        # _token - это приватное поле (по соглашению в Python).
        # Хранит токен только в памяти текущего процесса (не в файле).
        # None означает, что токен не получен или не валиден.
        self._token = None

    def _ensure_auth(self):
        """
            Гарантирует наличие валидного токена.
            Логика автоматической авторизации (умной):
                1. Если токен уже есть в памяти - возвращаем его.
                2. Если нет - пробуем использовать ключ из .env и проверяет его валидность
                3. Если ключ невалиден или отсутствует - получаем новый через API и сохраняем в .env.
            Такой подход делает клиент устойчивым к истечению ключей и смене окружения.
        """
        # еЕсли токен уже получен в текущей сессии в памяти - сразу возвращаем его (кэш).
        if self._token is not None:
            return self._token

        # Пытаемся использовать сохранённый ключ из .env.
        saved_key = os.getenv("YOUGILE_CURRENT_KEY")
        if saved_key:
            self._token = saved_key
            # Проверка валидности: делаем лёгкий запрос к API.
            # Если сервер вернёт 401 - ключ протух, то сбрасываем его.
            try:
                test_resp = requests.get(
                    f"{self.base_url}/api-v2/projects",
                    headers={"Authorization": f"Bearer {self._token}"}
                )
                if test_resp.status_code == 401:
                    # Ключ невалидный - сбрасываем, чтобы получить новый.
                    self._token = None
            except Exception:
                # Любая ошибка сети/соединения - считаем ключ непригодным.
                self._token = None

        # Если токена всё ещй нет (не было в .env или протух)  - запрашиваем новый.
        if self._token is None:
            url = f"{self.base_url}/api-v2/auth/keys"
            payload = {
                "login": self.login,
                "password": self.password,
                "companyId": self.company_id
            }
            resp = requests.post(url, json=payload)
            # raise_for_status() выдаст исключение, если сервер вернул ошибку (4хх/5хх).
            # Это защищает от "тихих" сбоев при получении ключа.

            print("🔍 Отправляем запрос на получение ключа:")
            print("URL:", url)
            print("Payload:", payload)
            print("Ответ статус:", resp.status_code)
            print("Тело ответа:", resp.text)
            resp.raise_for_status()
            self._token = resp.json()["key"]

            # Сразу сохраняем новый ключ в .env, чтобы следующие запуски тестов
            # не делали лишний запрос на получение ключа.
            from dotenv import set_key
            set_key(".env", "YOUGILE_CURRENT_KEY", self._token)

        return self._token

    def _headers(self):
        """
            Возвращает HTTP-заголовки для запроса.
            Обязательно вызывает _ensure_auth(), чтобы гарантировать валидный токен.
            Content-Type: application/json нужен для корректной передачи payload.
            Authorization: Bearer <token> - стандарт API YouGile для аутентификации.
        """
        token = self._ensure_auth()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def post(self, endpoint, payload):
        """
            Выполняет HTTP POST-запрос к указанной конечной точки (endpoint).
            Автоматически подставляет base_url и добавляет заголовки с токена.
            Удобно для создания сущностей (проекты, задачи и так далее).
        """
        url = f"{self.base_url}/{endpoint}"
        return requests.post(url, json=payload, headers=self._headers())

    def get(self, endpoint):
        """
            Выполняет HTTP GET-запрос.
            Используется для получения списков и деталей.
            Токен и заголовки добавляются автоматически.
        """
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, headers=self._headers())

    def put(self, endpoint, payload):
        """
            Выполняет HTTP PUT-запрос (частичное/полное обновление).
            Часто используется для изменения полей.
        """
        url = f"{self.base_url}/{endpoint}"
        return requests.put(url, json=payload, headers=self._headers())
