from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Универсиализация тестов для локалки и удалёнке
BASE_URL = "http://localhost:9999" # Замените на "https://httpbin.org"

# Ход теста:
def test_navigation():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 1. Откройте главную страницу
    driver.get(BASE_URL)

    # Найдите и кликните на ссылку /forms/post.    Для удалённой версии ['HTML form']
    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "/forms/post")))
    link.click()

    # Проверьте, что URL изменился на /forms/post.   http://127.0.0.1:9999/post
    assert "/forms/post" in driver.current_url

    # Вернитесь назад на главную страницу.     driver.back()
    driver.back()

    # Проверьте, что вернулись на на главную страницу
    assert driver.current_url == BASE_URL + "/"

    driver.quit()
