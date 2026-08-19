# test_03_shop.py
"""
Тест для интернет-магазина (без сканирования PDF)
Сценарий
    - Запуск браузера
    - Авторизация
    - Добавление 3-х товаров в корзину
    - Проверка корзины (значок кол-ва)
    - Переход в корзину
    - Проверка товаров в корзине
    - Оформление заказа
    - Проверка итоговой суммы
    - Вывод в консоль результатов
    - Скриншот
    - Закрытие браузера
"""

import os, allure
from selenium import webdriver
from pages.login_page import LoginPage

@allure.feature("Интернет-магазин")
@allure.story("Оформление заказа")
@allure.title("Проверка итоговой суммы заказа $58.29")
@allure.description("Авторизация, добавление 3 товаров, оформление, проверка суммы")
@allure.severity(allure.severity_level.CRITICAL)  # CRITICAL → так как работа всех проверяемых элементов очень важна
def test_shop():
    with allure.step("1. Запустить браузер Firefox"):
        # 1. Запускаем FireFox браузер
        driver = webdriver.Firefox()
        driver.maximize_window()
    with allure.step("2. Создать объект класса страницы логина"):
        # 2. Создаём объект страницы логина
        login_page = LoginPage(driver)

    with allure.step("3. Открыть страницу и авторизоваться"):
        # 3. Открываем страницу и авторизуемся
        login_page.open()
        inventory_page = login_page.login("standard_user", "secret_sauce")

    with allure.step("4. Добавить товары в корзину"):
        # 4. Добавляем товары (используем короткие имена)
        items = ["backpack", "bolt-t-shirt", "onesie"]
        for item in items:
            inventory_page.add_item_to_cart(item)

    with allure.step("5. Проверить количество товаров в корзине (на значке корзины)"):
        # 5. проверяем, что в корзине три товара
        assert inventory_page.get_cart_count() == 3, "В корзине 3 товара"

    with allure.step("6. Перейти в корзину"):
        # 6. Переход в корзину
        cart_page = inventory_page.go_to_cart()

    with allure.step("7. Проверить названия товаров в корзине"):
        # 7. Проверяем, что в корзине лежат товары
        expected_names = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        actual_names = cart_page.get_item_names()
        assert sorted(actual_names) == sorted(expected_names), "Набор товара не совпадает"

    with allure.step("8. Оформить заказ"):
        # 8. Оформляем заказ
        checkout_step_one = cart_page.proceed_to_checkout()
        checkout_step_two = checkout_step_one.fill_customer_info("Николай", "Сапронов", "111672")

    with allure.step("9. Проверить итоговую сумму"):
        # 9. Проверяем итоговую сумму
        total = checkout_step_two.get_total()
        assert total == "$58.29", f"Ожидалось $58.29, получено {total}"

    with allure.step("10. Вывести результат в консоль"):
        # 10. Вывод в консоль
        print("\n" + "=" * 50)
        print("🛒  РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА)")
        print("=" * 50)
        print(f" ✅ Товары добавлены: {', '.join(expected_names)}")
        print(f" ✅ Итоговая сумма: {total} (соответствует ожиданиям в $58.29)")
        print("=" * 50 + "\n")

    with allure.step("11. Сделать скриншот"):
        # 11. Скриншот
        os.makedirs("screen_07-img", exist_ok=True)
        driver.save_screenshot("screen_07-img/test03_shop.png")
        print("📸  Скриншот сохранён в папку screen_07-img")

    with allure.step("12. Закрыть браузер"):
        # 12. Закрываем Браузер
        driver.quit()
