import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 1. Откройте страницу https://the-internet.herokuapp.com/dynamic_loading/2
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    driver.maximize_window()

    # 2. Найдите и нажмите на кнопку "Start"
    start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']")))
    start_button.click()

    # 3. Дождитесь появления текста "Hello World!"
    #    Текст находится внутри элемента <h4>, который лежит внутри блока с id="finish"
    helo_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4")))

    # 4. Сделайте скриншот страницы
    os.makedirs("screenshot_img", exist_ok=True)    # Автоматически создаём папку для скриншотов
    driver.save_screenshot("screenshot_img/dynamic_loading.png") # Надо указывать существующую папку

    # 5. Проверьте, что появившийся текст равен "Hello World!"
    assert helo_element.text == "Hello World!"

    # 6. Закрываемся
    driver.quit()
