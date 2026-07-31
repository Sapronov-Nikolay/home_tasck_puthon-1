# setup_env.py
# Первоначальная настройка: создаёт .env, получает CompanyId и API-ключ.
# Запускается один раз.

import os, requests
from dotenv import load_dotenv, set_key

# Загружаем переменные из существующего .env (если он уже есть).
# Если нет — ничего страшного, дальше скрипт сам всё создаст.
load_dotenv()   # загружаем переменные из .env (файл в корне)

# Базовый URL API YouGile (можно переопределить в .env).
BASE_URL = os.getenv("YOUGILE_URL", "https://ru.yougile.com")

# Пытаемся взять логин/пароль из переменных окружения.
LOGIN = os.getenv("YOUGILE_LOGIN")
PASSWORD = os.getenv("YOUGILE_PASSWORD")

# Если логин/пароль не указаны - запрашиваем
# Если в .env логина/пароля нет — запрашиваем у пользователя вручную.
# Так скрипт можно запускать и без предварительного заполнения .env.
if not LOGIN:
    LOGIN = input("Введите ваш логин в YouGile: ")
if not PASSWORD:
    PASSWORD = input("Введите виш пароль: ")

print("\n🔑 Получаем CompanyId...")
try:
    # Запрос для получения списка компаний по логину/паролю.
    resp = requests.post(f"{BASE_URL}/api-v2/auth/companies", json={
        "login": LOGIN,
        "password": PASSWORD
    })
    resp.raise_for_status()
    companies = resp.json()

    # Проверка: если список компаний пустой — тогда это значит, логин/пароль не подходят.
    if not companies:
        print("❌ Компании не найдены. Проверьте логин и пароль.")
        exit(1)

    # Берём ID первой компании из списка.
    company_id = companies[0]["id"]
    print(f"✅ CompanyId получен: {company_id}")
except Exception as e:
    # Любая ошибка на этом этапе — критическая: без CompanyId дальше нельзя действовать.
    print(f"❌ Ошибка получения CompanyId: {e}")
    exit(1)

print("\n🔑 Получен API-ключ... (токен)")
try:
    # Запрос на получение API-ключа: нужны логин, пароль и CompanyId.
    resp = requests.post(f"{BASE_URL}/api-v2/auth/keys", json={
        "login": LOGIN,
        "password": PASSWORD,
        "company_id": company_id
    })
    resp.raise_for_status()
    # Из ответа берём только сам ключ.
    api_keys = resp.json()["keys"]
    # Выводим первые 20 символов, чтобы не светить весь ключ в логах.
    print(f"✅ API-ключ (токен) получен: {api_key[:20]}...")
except Exception as e:
    print(f"❌ Ошибка получения API-ключа: {e}")
    exit(1)

# set_key создаст .env, если его нет (создастся в той же папке, где запущен скрипт)
env_file = ".env"

# set_key автоматически создаст .env, если его нет, и запишет/обновит переменные.
set_key(env_file, "YOUGILE_URL", BASE_URL)
set_key(env_file, "YOUGILE_LOGIN", LOGIN)
set_key(env_file, "YOUGILE_PASSWORD", PASSWORD)
set_key(env_file, "YOUGILE_COMPANY_ID", company_id)
set_key(env_file, "YOUGILE_CURRENT_KEY", api_key)

print("\n✅ .env создан и заполнен.")
print("   Теперь можно запускать тесты: pytest tests/test_projects.py -v")
