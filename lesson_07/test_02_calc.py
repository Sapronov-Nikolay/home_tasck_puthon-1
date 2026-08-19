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

import os, allure
from selenium import webdriver
from pages.calculator_page import CalculatorPage

@allure.feature("Калькулятор")
@allure.story("Базовые арифметические операции")
@allure.title("Проверка сложения 7 + 8 = 15 с задержкой 45 секунд")
@allure.description("Калькулятор медленно вычисляет, ждём результат 45 секунд")
@allure.severity(allure.severity_level.CRITICAL)  # CRITICAL → так как работа всех проверяемых элементов очень важна
def test_calc():
    with allure.step("1. Запустить браузер Chrome"):
        # 1. Запускаем Chrome
        driver = webdriver.Chrome()
        driver.maximize_window()

    with allure.step("2. Создать объект класса страницы калькулятора"):
        # 2. Создаём объект страницы
        calc_page = CalculatorPage(driver)

    with allure.step("3. Открыть страницу калькулятора"):
        # 3. Открыть страницу
        calc_page.open()

    with allure.step("4. Установить задержку в 45 секунд"):
        # 4. Установить задержку в 45 секунд по заданию
        calc_page.set_delay(45)

    with allure.step("5. Нажать кнопки: 7, +, 8, ="):
        # 5. Набор вычисления
        calc_page.click_button("7")
        calc_page.click_button("+")
        calc_page.click_button("8")
        calc_page.click_button("=")

    with allure.step("6. Ожидать результат '15' (до 50 секунд) → Если результата нет, - падаем. (Не вечно же ждать)"):
        # 6. Ждём результата вычисления результата "15" (до 50 секунд)
        calc_page.wait_for_result("15", timeout=50)

    with allure.step("7. Получить результат"):
        # 7. Получаем фактический результат
        result = calc_page.get_result()

    with allure.step("8. Проверить полученный результат"):
        # 8. Проверить результат (assert)
        assert result == "15", f"Ожидалось 15 и получили {result}"

    with allure.step("9. Вывести результат в консоль"):
        # 9. Вывод в консоль для пользователя
        print("\n" + "=" * 50)
        print("🔢  РЕЗУЛЬТАТ КАЛЬКУЛЯТОРА")
        print("=" * 50)
        print(f" ✅ 7 + 8 = {result}, (ожидалось: 15)")
        print("=" * 50 + "\n")

    with allure.step("10. Сделать скриншот"):
        # 10. Делаем скриншот
        os.makedirs("screen_07-img", exist_ok=True)
        driver.save_screenshot(f"screen_07-img/test02_calc.png")

    with allure.step("11. Закрыть браузер"):
        # 11. Закрываем браузер
        driver.quit()
