# key_manager.py
# Управление API-ключами: просмотр, очистка с сохранением одного.
# После очистки автоматически обновляет токены в .env.
# ВАЖНО: скрипт требует логин/пароль и COMPANY_ID из .env.

import os
import sys
import requests
from dotenv import load_dotenv, set_key

# Загружаем переменные окружения из .env (если файл есть).
# Если .env нет — скрипт выдаст ошибку при попытке взять переменные.
load_dotenv()

# Считываем настройки из .env для работы с API YouGile.
BASE_URL = os.getenv("YOUGILE_URL")
LOGIN = os.getenv("YOUGILE_LOGIN")
PASSWORD = os.getenv("YOUGILE_PASSWORD")
COMPANY_ID = os.getenv("YOUGILE_COMPANY_ID")
CURRENT_KEY = os.getenv("YOUGILE_CURRENT_KEY")

# Проверка: если чего-то не хватает — лучше упасть сразу, чем потом в середине очистки.
if not all([BASE_URL, LOGIN, PASSWORD, COMPANY_ID]):
    print("❌ Ошибка: не хватает переменных в .env: YOUGILE_URL, YOUGILE_LOGIN, YOUGILE_PASSWORD, YOUGILE_COMPANY_ID")
    print("💡 Запустите сначала setup_env.py, чтобы создать .env.")
    sys.exit(1)

def get_all_keys():
    """
    Получить список всех API-ключей для компании.
    Возвращает список словарей (каждый — один ключ).
    """
    url = f"{BASE_URL}/api-v2/auth/keys/get"
    payload = {
        "login": LOGIN,
        "password": PASSWORD,
        "companyId": COMPANY_ID
    }
    # Отправляем POST-запрос, чтобы получить список ключей.
    resp = requests.post(url, json=payload)
    # Если сервер вернул ошибку (4-ую/5-ую) — сразу выдаётся исключение.
    resp.raise_for_status()
    return resp.json()

def delete_key(key_value, current_key):
    """
    Удалить конкретный API-ключ по его значению.
    current_key — это ключ, которым авторизуемся для выполнения DELETE.
    Возвращает True, если удаление прошло успешно (HTTP 200).
    """
    url = f"{BASE_URL}/api-v2/auth/keys/{key_value}"
    # Для удаления используем Bearer-авторизацию текущим ключом.
    headers = {"Authorization": f"Bearer {current_key}"}
    resp = requests.delete(url, headers=headers)
    return resp.status_code == 200

def list_keys():
    """
    Вывести список всех API-ключей в читаемом виде.
    Помечает текущий ключ (который указан в .env).
    """
    try:
        keys = get_all_keys()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return

    print("\n" + "=" * 70)
    print("🔑 СПИСОК ВСЕХ API-КЛЮЧЕЙ")
    print("=" * 70)
    print(f"📊 Всего ключей: {len(keys)}")
    print("=" * 70)

    for i, key_data in enumerate(keys, 1):
        key_value = key_data.get("key", "НЕТ ЗНАЧЕНИЯ")
        timestamp = key_data.get("timestamp", "неизвестно")
        # Помечаем, какой ключ сейчас считается «текущим» в .env.
        is_current = " ← ТЕКУЩИЙ" if CURRENT_KEY and key_value == CURRENT_KEY else ""
        print(f"{i:2}. КЛЮЧ: {key_value}")
        print(f"   ДАТА: {timestamp}{is_current}")
        print("-" * 70)

    print("=" * 70)
    print("💡 Для очистки старых ключей выполните:")
    print("   python key_manager.py --clean")
    print("=" * 70 + "\n")


def clean_keys(keep_key=None):
    """
    Удалить все API-ключи, кроме одного (keep_key).
    Если keep_key не передан, используется CURRENT_KEY из .env.
    Если и CURRENT_KEY нет — автоматически создаётся новый ключ.
    После очистки обновляет .env, чтобы тесты использовали актуальный ключ.
    Это чтобы убрать "головную боль" и не думать о ключах
    """
    # Определяем, какой ключ нужно сохранить.
    if keep_key is None:
        keep_key = CURRENT_KEY

    # Если даже CURRENT_KEY не задан — создаём новый ключ.
    if not keep_key:
        print("🔑 Сохраняемый ключ не задан, получаем новый...")
        try:
            resp = requests.post(f"{BASE_URL}/api-v2/auth/keys", json={
                "login": LOGIN,
                "password": PASSWORD,
                "companyId": COMPANY_ID
            })
            resp.raise_for_status()
            keep_key = resp.json()["key"]
            print(f"✅ Получен новый ключ: {keep_key[:20]}...")
        except Exception as e:
            print(f"❌ Ошибка получения ключа: {e}")
            return

    print("\n" + "=" * 60)
    print("🧹 ОЧИСТКА СТАРЫХ API-КЛЮЧЕЙ")
    print("=" * 60)

    try:
        keys = get_all_keys()
    except Exception as e:
        print(f"❌ Ошибка получения списка: {e}")
        return

    print(f"📊 Найдено ключей: {len(keys)}")
    print(f"🔑 Сохраняемый: {keep_key[:20]}...")

    deleted = 0
    skipped = 0

    for key in keys:
        key_value = key["key"]
        # Пропускаем ключ, который мы решили оставить.
        if key_value == keep_key:
            print(f"⏭️  Пропускаем: {key_value[:20]}...")
            skipped += 1
            continue

        # Пытаемся удалить остальные ключи.
        if delete_key(key_value, keep_key):
            print(f"✅ Удалён: {key_value[:20]}...")
            deleted += 1
        else:
            print(f"⚠️  Не удалось удалить: {key_value[:20]}... (возможно, уже удалён)")

    print("=" * 60)
    print(f"✅ Удалено: {deleted}")
    print(f"⏭️  Пропущено: {skipped}")
    print(f"📊 Осталось ключей (токенов): {len(keys) - deleted}")
    print("=" * 60)

    # Обновляем .env, чтобы в нём был актуальный ключ для тестов.
    set_key(".env", "YOUGILE_CURRENT_KEY", keep_key)
    print(f"✅ .env обновлён: YOUGILE_CURRENT_KEY = {keep_key[:20]}...")
    print("   Теперь тесты будут использовать этот ключ (токен).\n")


if __name__ == "__main__":
    # Обрабатываем аргументы командной строки.
    # Это позволяет запускать скрипт в разных режимах без изменения кода.
    # Пишем флаги для команд, чтоб были варианты действий из CMD
    if "--list" in sys.argv:
        list_keys()
    elif "--clean" in sys.argv:
        keep_key = None
        # Если указан флаг --keep, берём следующий аргумент как ключ для сохранения.
        if "--keep" in sys.argv:
            idx = sys.argv.index("--keep") + 1
            if idx < len(sys.argv):
                keep_key = sys.argv[idx]
            else:
                print("❌ Ошибка: после --keep укажите значение ключа")
                sys.exit(1)
        clean_keys(keep_key)
    else:
        # Если аргументы не переданы — выводим справку.
        print("""Использование:
    python key_manager.py --list
        Показать список всех API-ключей (токенов).
    python key_manager.py --clean
        Удалить все ключи (токены), кроме текущего (из .env). Если текущего нет — создать новый.
    python key_manager.py --clean --keep <ключ>
        Удалить все ключи (токены), кроме указанного.
        """)
