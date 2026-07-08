from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Зафиксирована ссылка главной странице
BASE_URL = "https://httpbin.org"

# Ход теста
def test_form_submition():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # 1. Открываем главную страницу
    driver.get(BASE_URL)

    # 2. Разворачиваемся на всю
    driver.maximize_window()

    # 3. Находим кнопку-ссылку "HTML form"
    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "HTML form")))
    link.click()    # Клик по ссылке

    # 4. Проверьте, что URL изменился на /forms/post.
    assert "/forms/post" in driver.current_url

    # 5. Найдите поле ввода с названием custname. → ["custname"]
    name_field = wait.until(EC.presence_of_element_located((By.NAME, "custname")))

    # 6. Вводим Имечко
    name_field.send_keys("Николай")

    # 7. Находим кнопку Submit и нажимаем на неё изо всех сил
    submit_btm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit order']")))
    submit_btm.click()  # Кликаем по ней

    # 8. Проверяем, что перешли на новую ссылку → значит ввод данных отправился
    assert "/forms/post" in driver.current_url

    # 9. Ждём 2 секунды
    sleep(2)

    # 10. Открываем главную страницу
    driver.get(BASE_URL)

    # 11. Ждём 2 секунды
    sleep(2)

    # 12. Переходим на специальную страницу
    driver.get(f"{BASE_URL}/links/10")

    # 13. Ждём 2 секунды
    sleep(2)

    # 14. Находим ссылки определяем их в переменную
    links = driver.find_elements(By.TAG_NAME, "a")

    # 15. Проверяем что в переменной 9 ссылок
    assert len(links) == 9

    # 16. gробегаемся по ссылкам, убеждаемся что они все работают
    for link in links:
        assert link.is_displayed()

    # 17. Проверяем, что первая ссылка как текст
    assert "1" in links[0].text

    # 18. Выходим из теста
    driver.quit()
