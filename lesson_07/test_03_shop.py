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

import os
from selenium import webdriver
from pages.login_page import LoginPage

def test_shop():
    # 1. Запускаем FireFox браузер
    driver = webdriver.Firefox()
    driver.maximize_window()

    # 2. Создаём объект страницы логина
    login_page = LoginPage(driver)

    # 3. Открываем страницу и авторизуемся
    login_page.open()
    inventory_page = login_page.login("standard_user", "secret_sauce")

    # 4. Добавляем товары (используем короткие имена)
    items = ["backpack", "bolt-t-shirt", "onesie"]
    for item in items:
        inventory_page.add_item_to_cart(item)

    # 5. проверяем, что в корзине три товара
    assert inventory_page.get_cart_count() == 3, "В корзине 3 товара"

    # 6. Переход в корзину
    cart_page = inventory_page.go_to_cart()

    # 7. Проверяем, что в корзине лежат товары
    expected_names = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
    actual_names = cart_page.get_item_names()
    assert sorted(actual_names) == sorted(expected_names), "Набор товара не совпадает"

    # 8. Оформляем заказ
    checkout_step_one = cart_page.proceed_to_checkout()
    checkout_step_two = checkout_step_one.fill_customer_info("Николай", "Сапронов", "111672")

    # 9. Проверяем итоговую сумму
    total = checkout_step_two.get_total()
    assert total == "$58.29", f"Ожидалось $58.29, получено {total}"

    # 10. Вывод в консоль
    print("\n" + "=" * 50)
    print("🛒  РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА)")
    print("=" * 50)
    print(f" ✅ Товары добавлены: {', '.join(expected_names)}")
    print(f" ✅ Итоговая сумма: {total} (соответствует ожиданиям в $58.29)")
    print("=" * 50 + "\n")

    # 11. Скриншот
    os.makedirs("screen_07-img", exist_ok=True)
    driver.save_screenshot("screen_07-img/test03_shop.png")
    print("📸  Скриншот сохранён в папку screen_07-img")

    # 12. Закрываем Браузер
    driver.quit()
