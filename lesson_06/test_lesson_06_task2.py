import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_session_storage_auth():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # Создаём заранее папку для складирования скриншотов этого теста
    os.makedirs("screenshot_gitflic", exist_ok=True)
    # Шаги

    # 1. Откройте страницу https://gitflic.ru/.
    driver.get("https://gitflic.ru/")
    driver.maximize_window()

    # -------- ПЕРВЫЙ ПОЛЬЗОВАТЕЛЬ (nikolay_1) --------
    # 2. Установите cookie пользователя 1.
    driver.add_cookie({
        "name": "SESSION",
        "value": "MjUzM2E5YWUtYWVkMi00OTM4LWI0NWItMGZlMWZkZTZhM2Vl",
        "domain": ".gitflic.ru",
        "path": "/",  #  Рекомендуется указывать для работы куки на всех страницах сайта
    })
    # Убираем баннер для подтверждения куки
    driver.add_cookie({
        "name": "cookiesAccepted",
        "value": "true",
        "domain": ".gitflic.ru",
        "path": "/",
    })

    # 3. Обновите страницу (для применения куки).
    driver.refresh()
    wait.until(EC.presence_of_element_located(((By.TAG_NAME, "body")))) # ← Ждём загрузки тела DOM

    # 4. Перейдите на страницу пользователя 1.
    driver.get("https://gitflic.ru/user/nikolay_1")
    wait.until(EC.presence_of_element_located(((By.TAG_NAME, "body")))) # ← Ждём загрузки тела DOM

    # 5. Сохраните текущий URL.
    url_user1 = driver.current_url
    driver.save_screenshot("screenshot_gitflic/user1_nikolay_1.png")

    # -------- ВЫХОД ИЗ АККАУНТА --------
    # 6. Разлогиньтесь (очистите куки).
    driver.delete_all_cookies()
    driver.refresh()
    wait.until(EC.presence_of_element_located(((By.TAG_NAME, "body")))) # ← Ждём загрузки тела DOM

    # -------- ВТОРОЙ ПОЛЬЗОВАТЕЛЬ (nikolay_2) --------
    # 7. Установите cookie пользователя 2.
    driver.add_cookie({
        "name": "SESSION",
        "value": "ZTBjNTdmZDktZTMxOC00OTQ3LWFhODctZDIwMWExNmU0M2Rm",
        "domain": ".gitflic.ru",
        "path": "/",
    })
    # Убираем баннер для подтверждения куки
    driver.add_cookie({
        "name": "cookiesAccepted",
        "value": "true",
        "domain": ".gitflic.ru",
        "path": "/",
    })

    # 8. Обновите страницу. (для применения куки).
    driver.refresh()
    wait.until(EC.presence_of_element_located(((By.TAG_NAME, "body")))) # ← Ждём загрузки тела DOM

    # 9. Перейдите на страницу пользователя 2.
    driver.get("https://gitflic.ru/user/nikolay_2")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))) # ← Ждём загрузки тела DOM

    # 10. Сохраните текущий URL.
    url_user2 = driver.current_url
    driver.save_screenshot("screenshot_gitflic/user2_nikolay_2.png")

    # 12. Проверьте, что URL для пользователя 1 и пользователя 2 различаются.
    assert url_user1 != url_user2, "URL профилей одинаковые - значит что-то не так. проверьте CUKIES"

    # Закрываемся
    driver.quit()
