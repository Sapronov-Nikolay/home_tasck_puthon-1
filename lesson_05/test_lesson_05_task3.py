from httpbin import links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Универсиализация тестов для локалки и удалёнке
BASE_URL = "http://localhost:9999" # Замените на "https://httpbin.org"

# Ход теста:
def test_multiple_elements():
    # 1. Запускаем браузер
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Если что-то грузится, ждём максимум 10 секунд
    wait = WebDriverWait(driver, 10)

    # 2. Откройте страницу http://127.0.0.1:9999/links/10/0.
    driver.get(f"{BASE_URL}/links/10")

    # Найдите все ссылки на странице (тег <a>).
    # 3. Ждём, пока на странице появится хотя бы одна ссылка - это гарантия загрузки страницы
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # 4. Проверьте, что количество ссылок равно 9.
    #    На странице всего 9 ссылок, а активная это текст цифры find_elements (во множ. числе) возвращает список
    links = driver.find_elements(By.TAG_NAME, "a")


    # 5. Проверьте, что все ссылки отображаются на странице.
    assert len(links) == 9

    # 6. Проверяем, что все ссылки отображаются на странице
    for link in links:
        assert link.is_displayed()

    # 7. Проверьте, что текст первой ссылки содержит "1".
    assert "1" in links[0].text

    # 8. Закрываемся
    driver.quit()
