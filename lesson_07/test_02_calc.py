# test_02_calc.py
"""
Тест для медленного калькулятора
Сценарий такой:
    - Запуск браузера
    - Открыть страницу
    - Установить задержку в 45 сек
    - Набрать вычисление на калькуляторе 7 + 8 =
    - Дождаться результата вычисления 15
    - Проверить результат через assert
    - Вывести информацию в консоль
    - сделать скриншот
    - закрыть браузер
"""

import os
from selenium import webdriver
from pages.calculator_page import CalculatorPage

def test_calc():
    # 1. Запускаем Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 2. Создаём объект страницы
    calc_page = CalculatorPage(driver)

    # 3. Открыть страницу
    calc_page.open()

    # 4. Установить зедержку в 45 секунд по заданию
    calc_page.set_delay(45)

    # 5. Набор вычисления
    calc_page.click_button("7")
    calc_page.click_button("+")
    calc_page.click_button("8")
    calc_page.click_button("=")

    # 6. Ждём результата вычисления результата "15" (до 50 секунд)
    calc_page.wait_for_result("15", timeout=50)

    # 7. Получаем фактический результат
    result = calc_page.get_result()

    # 8. Проверить результат (assert)
    assert result == "15", f"Ожидалось 15 и получили {result}"

    # 9. Вывод в консоль для пользователя
    print("\n" + "=" * 50)
    print("🔢  РЕЗУЛЬТАТ КАЛЬКУЛЯТОРА")
    print("=" * 50)
    print(f" ✅ 7 + 8 = {result}, (ожидалось: 15)")
    print("=" * 50 + "\n")

    # 10. Делаем скриншот
    os.makedirs("screen_07-img", exist_ok=True)
    driver.save_screenshot(f"screen_07-img/test02_calc.png")

    # 11. Закрываем браузер
    driver.quit()