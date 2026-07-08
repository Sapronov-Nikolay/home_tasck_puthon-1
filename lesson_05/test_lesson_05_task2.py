from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Универсиализация тестов для локалки и удалёнке
BASE_URL = "http://localhost:9999" # Замените на "https://httpbin.org"

# Ход теста:
def test_form_submition():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # Откройте страницу http://127.0.0.1:9999/forms/post. сразу переход на этот сайт
    driver.get(f"{BASE_URL}/forms/post")

    # Найдите поле ввода с названием custname. → ["custname"]
    name_field = wait.until(EC.element_to_be_clickable((By.NAME, "custname")))
    # Введите в него ваше имя.   →  Николай
    name_field.send_keys("Николай")

    # Найдите кнопку Submit и нажмите на нее.  →  Submit order
    submit_btm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit order']")))

    submit_btm.click()

    # Проверьте, что после нажатия URL изменился.  → http://127.0.0.1:9999/post
    assert "/post" in driver.current_url

    driver.quit()

