import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_calc():
    # 1. Выбираем браузер
    driver = webdriver.Chrome()
    # 2. Ставим ждуна на максимально допустимое ожидание
    wait = WebDriverWait(driver, 50)
    # 3. Открываем указанную ссылку для тестирования
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    # 4. Разворачиваем браузер на весь экран
    driver.maximize_window()

    # 5. Ищем элемент ввода задержки расчётов по локатору
    delay_input = wait.until(EC.presence_of_element_located((By.ID, "delay")))
    # 5.1 Очищаем поле от чисел по уполчанию (5)
    delay_input.clear()
    # 5.2 Вводим задержку из задания (45)
    delay_input.send_keys("45")

    # 6. Набираем по кнопкам вычисления: 7 + 8 =
    btn_7 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='7']")))
    btn_7.click()

    btn_plus = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='+']")))
    btn_plus.click()

    btn_8 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='8']")))
    btn_8.click()

    btn_rovno = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='=']")))
    btn_rovno.click()

    # 7. Смотрим результат вычислений в элементе: <div class="screen"></div> ожидается (15)
    wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))

    # 8. Получаем, вытягиваем результат чтоб с ним работать дальше
    screen = driver.find_element(By.CLASS_NAME, "screen")
    result_text = screen.text

    # 9. Делаем скриншот области для просмотра результата
    os.makedirs("screen_06K-img", exist_ok=True)
    driver.save_screenshot(f"screen_06K-img/test02_calc.png")

    # 10. Проверяем, что результат действительно равен (15)
    assert  result_text == "15", f"Ожидалось 15 и получили {result_text}"

    # 11. Выводим в консоль красивый вывод
    print("\n" + "="*50)
    print("🔢  РЕЗУЛЬТАТ КАЛЬКУЛЯТОРА")
    print("="*50)
    print(f" ✅ 7 + 8 = {result_text}, (ожидалось: 15)")
    print("="*50 + "\n")

    # 12. Выходим из теста
    driver.quit()
