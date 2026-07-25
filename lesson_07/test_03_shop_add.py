# test_03_shop_add.py
"""
Тест магазина со скачиванием PDF.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage


def test_shop_pdf():
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

    # -------- Запуск браузера --------
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    # -------- Основной сценарий --------
    login_page = LoginPage(driver)
    login_page.open()
    inventory_page = login_page.login("standard_user", "secret_sauce")

    items = ["backpack", "bolt-t-shirt", "onesie"]
    for item in items:
        inventory_page.add_item_to_cart(item)

    assert inventory_page.get_cart_count() == 3, "В корзине не 3 товара"

    cart_page = inventory_page.go_to_cart()
    expected_names = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]
    assert sorted(cart_page.get_item_names()) == sorted(expected_names), "Набор товаров не совпадает"

    checkout_step_one = cart_page.proceed_to_checkout()
    checkout_step_two = checkout_step_one.fill_customer_info("Николай", "Сапронов", "111672")

    total = checkout_step_two.get_total()
    assert total == "$58.29", f"Ожидалось $58.29, получено {total}"

    # -------- Finish и PDF --------
    complete_page = checkout_step_two.finish()
    driver.save_screenshot("screen_07-img/test03_shop_finish.png")

    complete_page.generate_pdf()
    print(" ⏳ Ожидаем скачивания PDF...")

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

    # Финальный вывод в консоль
    print("\n" + "=" * 50)
    print("🛒 РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА) С PDF")
    print("=" * 50)
    print(f"  ✅ Товары добавлены: {', '.join(expected_names)}")
    print(f"  ✅ Итоговая сумма: {total} (ожидалось $58.29)")
    print(f"  ✅ PDF-файл скачан: {pdf_file}")
    print("=" * 50 + "\n")

    # Закрываемся
    driver.quit()