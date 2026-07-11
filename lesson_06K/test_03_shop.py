import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shop():
    # 1. Выбираем браузер
    driver = webdriver.Firefox()
    # 2. Ставим ждуна с максимально допустимым ожидаем
    wait = WebDriverWait(driver, 10)
    # 3. открываем указанный целевой сайт
    driver.get("https://www.saucedemo.com/")
    # 4. Разворачиваем браузер на весь экран
    driver.maximize_window()

    # 5. Авторизация: дожидаемся загрузки формы ввода
    user_name = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    # 5.1 Чистим поле на случай если браузер автоподставил иные данные
    user_name.clear()
    user_name.send_keys("standard_user")

    # 5.2 Вводим пароль
    password = driver.find_element(By.ID, "password")
    # 5.3 Чистим поле пароля от мало ли каких данных
    password.clear()
    password.send_keys("secret_sauce")

    # 6. Нажимаем ввод и логинимся
    login_btn = driver.find_element(By.ID, "login-button")
    login_btn.click()

    # 7. Проверяем, что перешли на выбор товаров - залогинились.
    wait.until(EC.url_contains("inventory.html"))
    print(" Переход к выбору товаров успешен - ссылка соответствует .../inventory.html")

    # 8. Добавляем товары: список ID кнопок "Add to cart" для выбранных товаров
    items = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bolt-t-shirt",
        "add-to-cart-sauce-labs-onesie"
    ]

    # 9. Для каждого товара кликаем по кнопке и проверяем что она стала "Remove"
    for item_id in items:
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, item_id)))
        add_btn.click()
        # Проверяем, что кнопка изменила текст на "Remove"
        # Поищем кнопку по её id (удаляем add-to-cart-, добавляем "Remove"
        remove_id = item_id.replace("add-to-cart-", "remove-")
        remove_btn = wait.until(EC.element_to_be_clickable((By.ID, remove_id)))
        assert remove_btn.text == "Remove", f"Кнопка для {item_id} не стала 'Remove'"
        # Выводим в консоль результат проверки
        print(f" ✅ Товар {item_id} добавлен (кнопка стала Remove)")

    # 10. Проверяем, что в корзине отображается количество добавленных товаров и их там 3
    cart_badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text == "3", f"Ожидалось 3 товара, а попало {cart_badge.text}"
    # 11. Выводим в консольку эту чудную информацию
    print(f" ✅ Количество товаров на значке корзины {cart_badge.text} шт. Ожидалось 3 шт. СУПЕР 😀")

    # 12. Переходим в корзину: проверяем, что URL стал /cart.html
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    # 13. Проверяем, что URL стал /cart.html
    wait.until(EC.url_contains("cart.html"))
    print(" ✅ Переход в корзину выполнен - ссылка соответствует .../cart.html")

    # 14. Проверяем наличие товаров в корзине
    cart_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
    assert len(cart_items) == 3, f"В самой корзине должно быть 3 товара, а найдено {len(cart_items)} шт."
    # 15. Выводим и это в консольку
    print(f" ✅ Товаров в самой корзине {len(cart_items)} шт. Ожидалось 3 шт. СУПЕР 😀")

    # 16. Проверяем, что в корзину добавилось именно то, что выбирали.
    # Имена лежат в: <div class="inventory_item_name" data-test="inventory-item-name">expected_names</div>
    expected_names = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]
    actual_names = [] # Пустой список для добавления

    # 17. Перебираем элементы вложенные в корзину
    for cart_item in cart_items:
        name_elem = cart_item.find_element(By.CLASS_NAME, "inventory_item_name")
        actual_names.append(name_elem.text)
    assert sorted(actual_names) == sorted(expected_names), f"Ожидалось {expected_names}, а получены {actual_names}"
    # 18. Выводим в консоль
    print(f" ✅ Названия товаров {expected_names} = {actual_names} СУПЕР 😀")

    # 19. Оформляем заказ: нажимаем Checkout
    checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_btn.click()

    # 20. Убеждаемся что перешли на страницу оформления .../checkout-step-one.html
    wait.until(EC.url_contains("checkout-step-one.html"))
    # 21. Выводим сообщение в консоль
    print(" ✅ Переход к оформлению заказа выполнен - ссылка соответствует .../checkout-step-one.html")

    # 22. Дожидаемся загрузки полей формы оформления и определяем первое → Имя
    first_name = wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    # Чистим поле от возможных автозаполнений
    first_name.clear()
    # Заполняем чисто поле
    first_name.send_keys("Николай")

    # 23. Заолняем поле → Фамилия
    last_name = driver.find_element(By.ID, "last-name")
    # Чистим поле от возможных автозаполнений
    last_name.clear()
    # Заполняем чисто поле
    last_name.send_keys("Сапронов")

    # 24. Заполняем поле → Почтовый индекс
    postal_code = driver.find_element(By.ID, "postal-code")
    # Чистим поле от возможных автозаполнений
    postal_code.clear()
    # Заполняем чисто поле
    postal_code.send_keys("111672")

    # 25. Нажимаем кнопарик Continue
    continue_btn = driver.find_element(By.ID, "continue")
    continue_btn.click()
    wait.until(EC.url_contains("checkout-step-two.html"))
    # 26. Выводим в консоль
    print(" ✅ Преход страницу итогов выполнен  - ссылка соответствует .../checkout-step-two.html")

    # 27. Получаем итоговую сумму: она в конце страницы - нужен скролл
    # Скролим страницу до отображения <div class="summary_total_label" data-test="total-label">Total: $58.29</div>
    total_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", total_element)

    # 28. Читаем текст и извлекаем сумму
    total_text = total_element.text # Например, "Total: $58.29"
    total_value = total_text.replace("Total: ", "").strip()
    # 29. Выводим в консоль
    print(f"🛒  Итоговая сумма по данным страницы: {total_value}")

    # 30. Делаем скриншот финальной страницы
    os.makedirs("screen_06K-img", exist_ok=True)
    driver.save_screenshot("screen_06K-img/test03_shop.png")
    # 31. Выводим в консоль
    print("📸  Скриншот сохранён в папку screen_06K-img")

    # 32. Проверка итоговой суммы: сравниваем с ожидаемой суммы
    assert total_value == "$58.29", f"Ожидалось $58.29, а получено {total_value}"

    # 33. Выводим красивый итог в консоли
    print("\n" + "="*50)
    print("🛒  РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА)")
    print("="*50)
    print(f" ✅ Товары добавлены: {', '.join(expected_names)}")
    print(f" ✅ Итоговая сумма: {total_value} (соответствует ожиданиям в $58.29)")
    print("="*50 + "\n")

    # 34. Закрываем браузер
    driver.quit()
