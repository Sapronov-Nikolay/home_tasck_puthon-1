# test_03_shop_add.py
"""
Тест магазина со скачиванием PDF.
"""

import os, time, allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage

@allure.feature("Интернет-магазин")
@allure.story("Оформление заказа с PDF")
@allure.title("Проверка итоговой суммы и скачивание PDF")
@allure.description("Авторизация, добавление 3 товаров, оформление, скачивание PDF")
@allure.severity(allure.severity_level.CRITICAL)  # CRITICAL → так как работа всех проверяемых элементов очень важна
def test_shop_pdf():
    with allure.step("1. Настроить Firefox для скачивания PDF"):
        # -------- Настройки Firefox для скачивания PDF --------
        options = Options()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(current_dir, "PDF-order")
        os.makedirs(download_dir, exist_ok=True)

        options.set_preference("browser.download.dir", download_dir)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("pdfjs.disabled", True)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.download.manager.showWhenStarting", False)

    with allure.step("2. Запустить браузер Firefox с настройками"):
        # -------- Запуск браузера --------
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

    with allure.step("3. Создать объект класса страницы логина"):
        # -------- Основной сценарий --------
        login_page = LoginPage(driver)

    with allure.step("4. Открыть страницу и авторизоваться"):
        login_page.open()
        inventory_page = login_page.login("standard_user", "secret_sauce")

    with allure.step("5. Добавить товары в корзину"):
        items = ["backpack", "bolt-t-shirt", "onesie"]
        for item in items:
            inventory_page.add_item_to_cart(item)

    with allure.step("6. Проверить количество товаров в на значке корзины"):
        assert inventory_page.get_cart_count() == 3, "В на значке корзины не 3 товара"

    with allure.step("7. Перейти в саму корзину и сверить выборку товаров"):
        cart_page = inventory_page.go_to_cart()
        expected_names = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
        assert sorted(cart_page.get_item_names()) == sorted(expected_names), "Набор товаров не совпадает"

    with allure.step("8. Начать оформление заказа"):
        checkout_step_one = cart_page.proceed_to_checkout()

    with allure.step("9. Заполнить форму оформления заказа"):
        checkout_step_two = checkout_step_one.fill_customer_info("Николай", "Сапронов", "111672")

    with allure.step("10. Проверить итоговую сумму"):
        total = checkout_step_two.get_total()
        assert total == "$58.29", f"Ожидалось $58.29, получено {total}"

        # -------- Finish и PDF --------
    with allure.step("11. Завершить заказ"):
        complete_page = checkout_step_two.finish()
        driver.save_screenshot("screen_07-img/test03_shop_finish.png")

    with allure.step("12. Скачать PDF"):
        complete_page.generate_pdf()
        print(" ⏳ Ожидаем скачивания PDF...")

    with allure.step("13. Ожидать появление PDF-файла (до 30 сек → так как мы не хотим ждать его вечно)"):
        # Ожидание файла
        start_time = time.time()
        pdf_file = None
        while time.time() - start_time < 30:
            files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
            if files:
                pdf_file = files[0]
                break
            time.sleep(1)
        assert pdf_file is not None, "PDF-файл не появился"
        print(f" ✅ PDF-файл {pdf_file} скачан")

    with allure.step("14. Вывести результат в консоль"):
        # Финальный вывод в консоль
        print("\n" + "=" * 50)
        print("🛒 РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА) С PDF")
        print("=" * 50)
        print(f"  ✅ Товары добавлены: {', '.join(expected_names)}")
        print(f"  ✅ Итоговая сумма: {total} (ожидалось $58.29)")
        print(f"  ✅ PDF-файл скачан: {pdf_file}")
        print("=" * 50 + "\n")

    with allure.step("15. Закрыть браузер"):
        # Закрываемся
        driver.quit()
