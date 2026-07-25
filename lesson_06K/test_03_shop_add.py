import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def test_shop():
    # ============================================================
    # БЛОК НАСТРОЙКИ FIREFOX ДЛЯ СКАЧИВАНИЯ PDF
    # ============================================================

    # 1. Настройки Firefox для скачивания PDF в папку проекта
    """
        Oprions() - это объект, в котором хранятся настройки браузера
        Мы передаём его в webdriver.Firefox(), чтобы браузер запускался уже с нужными для скачивания настройками
    """
    options = Options()

    # 2. Получаем папку, где лежит текущий файл (test_03_shop_add.py)
    """
        __file__ - это специальная переменная Puthon, которая содержит путь к текущему файлу.
        os.path.abspath(__file__) - превращает относительный путь в абсолютный (полный)
        os.path.dirname(...) - берёт только папку, без имени файла
        В итоге current_dir = "I:/.../lesson_06K" - папка, где лежит этот тест
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    """
        os.path.join() - склеивает путь и название папки.
        В итоге download_dir = "I:/.../lesson_06K/PDF-ordef" - мы хотим, чтобы PDF сохранялся
        именно в папку, где находится тест, а не в корень проекта.
    """
    download_dir = os.path.join(current_dir, "PDF-order")

    # 3. Настройки Firefox
    """ Указываем Firefox, куда сохранять скачанный файл - в эту папку 'PDF-order' """
    options.set_preference("browser.download.dir", download_dir)

    """  Цифра 2 означает использовать пользовательнсую папку
         0 или 1 - это папка загрузок по умолчанию из параметров браузера """
    options.set_preference("browser.download.folderList", 2)

    """ Говорим Firefox: - Никогда не спрашивай, что делать с этим файлом, а сразу скачивай
        application/pdf -  MIME-тип - это означает - (Multipurpose Internet Mail Extensions — «многоцелевые расширения для интернет-почты») —
        это стандартизированный способ указать природу и формат данных,
        которые передаются через интернет. Проще говоря, он помогает программам (браузерам, серверам, почтовым клиентам)
        понять, как именно нужно обработать полученный контент:
        отобразить картинку, воспроизвести аудио, прочитать документ или что-то другое. """
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

    """ Отключаем встроенный просмотрщик PDF в Firefox. Если его не отключить,
        браузер может открыть PDF в новой вкладке, а не скачать"""
    options.set_preference("pdfjs.disabled", True)

    """ Всегда использовать указанную папку для скачиваний - не переспрашивать """
    options.set_preference("browser.download.useDownloadDir", True)

    """ Не показывать окно менеджера загрузок - чтобы не мешать тесту """
    options.set_preference("browser.download.manager.showWhenStarting", False)

    # 4. Создаём папку для скачивания PDF-файла
    """ exist_ok=True - это если папка уже существует, не выдавать ошибку.
        Это гарантирует, что папка есть до того, как браузер начнёт скачивание. """
    os.makedirs(download_dir, exist_ok=True)

    # 5. Выбираем браузер и вписываем туда настройки для опций загрузки options=options
    driver = webdriver.Firefox(options=options)
    # 6. Ставим ждуна с максимально допустимым ожидаем
    wait = WebDriverWait(driver, 10)
    # 7. открываем указанный целевой сайт
    driver.get("https://www.saucedemo.com/")
    # 8. Разворачиваем браузер на весь экран
    driver.maximize_window()

    # 9. Авторизация: дожидаемся загрузки формы ввода
    user_name = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    # 9.1 Чистим поле на случай если браузер автоподставил иные данные
    user_name.clear()
    user_name.send_keys("standard_user")

    # 9.2 Вводим пароль
    password = driver.find_element(By.ID, "password")
    # 9.3 Чистим поле пароля от мало ли каких данных
    password.clear()
    password.send_keys("secret_sauce")

    # 10. Нажимаем ввод и логинимся
    login_btn = driver.find_element(By.ID, "login-button")
    login_btn.click()

    # 11. Проверяем, что перешли на выбор товаров - залогинились.
    wait.until(EC.url_contains("inventory.html"))
    print(" Переход к выбору товаров успешен - ссылка соответствует .../inventory.html")

    # 12. Добавляем товары: список ID кнопок "Add to cart" для выбранных товаров
    items = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bolt-t-shirt",
        "add-to-cart-sauce-labs-onesie"
    ]

    # 13. Для каждого товара кликаем по кнопке и проверяем что она стала "Remove"
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

    # 14. Проверяем, что в корзине отображается количество добавленных товаров и их там 3
    cart_badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text == "3", f"Ожидалось 3 товара, а попало {cart_badge.text}"
    # 15. Выводим в консольку эту чудную информацию
    print(f" ✅ Количество товаров на значке корзины {cart_badge.text} шт. Ожидалось 3 шт. СУПЕР 😀")

    # 16. Переходим в корзину: проверяем, что URL стал /cart.html
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    # 17. Проверяем, что URL стал /cart.html
    wait.until(EC.url_contains("cart.html"))
    print(" ✅ Переход в корзину выполнен - ссылка соответствует .../cart.html")

    # 18. Проверяем наличие товаров в корзине
    cart_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
    assert len(cart_items) == 3, f"В самой корзине должно быть 3 товара, а найдено {len(cart_items)} шт."
    # 19. Выводим и это в консольку
    print(f" ✅ Товаров в самой корзине {len(cart_items)} шт. Ожидалось 3 шт. СУПЕР 😀")

    # 20. Проверяем, что в корзину добавилось именно то, что выбирали.
    # Имена лежат в: <div class="inventory_item_name" data-test="inventory-item-name">expected_names</div>
    expected_names = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]
    actual_names = [] # Пустой список для добавления

    # 21. Перебираем элементы вложенные в корзину
    for cart_item in cart_items:
        name_elem = cart_item.find_element(By.CLASS_NAME, "inventory_item_name")
        actual_names.append(name_elem.text)
    assert sorted(actual_names) == sorted(expected_names), f"Ожидалось {expected_names}, а получены {actual_names}"
    # 22. Выводим в консоль
    print(f" ✅ Названия товаров {expected_names} = {actual_names} СУПЕР 😀")

    # 23. Оформляем заказ: нажимаем Checkout
    checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_btn.click()

    # 24. Убеждаемся что перешли на страницу оформления .../checkout-step-one.html
    wait.until(EC.url_contains("checkout-step-one.html"))
    # 25. Выводим сообщение в консоль
    print(" ✅ Переход к оформлению заказа выполнен - ссылка соответствует .../checkout-step-one.html")

    # 26. Дожидаемся загрузки полей формы оформления и определяем первое → Имя
    first_name = wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    # Чистим поле от возможных автозаполнений
    first_name.clear()
    # Заполняем чисто поле
    first_name.send_keys("Николай")

    # 27. Заолняем поле → Фамилия
    last_name = driver.find_element(By.ID, "last-name")
    # Чистим поле от возможных автозаполнений
    last_name.clear()
    # Заполняем чисто поле
    last_name.send_keys("Сапронов")

    # 28. Заполняем поле → Почтовый индекс
    postal_code = driver.find_element(By.ID, "postal-code")
    # Чистим поле от возможных автозаполнений
    postal_code.clear()
    # Заполняем чисто поле
    postal_code.send_keys("111672")

    # 29. Нажимаем кнопарик Continue
    continue_btn = driver.find_element(By.ID, "continue")
    continue_btn.click()
    wait.until(EC.url_contains("checkout-step-two.html"))
    # 30. Выводим в консоль
    print(" ✅ Переход страницу итогов выполнен  - ссылка соответствует .../checkout-step-two.html")

    # 31. Получаем итоговую сумму: она в конце страницы - нужен скролл
    # Скролим страницу до отображения <div class="summary_total_label" data-test="total-label">Total: $58.29</div>
    total_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", total_element)

    # 32. Читаем текст и извлекаем сумму
    total_text = total_element.text # Например, "Total: $58.29"
    total_value = total_text.replace("Total: ", "").strip()
    # 33. Выводим в консоль
    print(f" 🛒 Итоговая сумма по данным страницы: {total_value}")

    # 34. Делаем скриншот финальной страницы
    os.makedirs("screen_06K-img", exist_ok=True)
    driver.save_screenshot("screen_06K-img/test03_shop.png")
    # 35. Выводим в консоль
    print(" 📸 Скриншот сохранён в папку screen_06K-img")

    # 36. Проверка итоговой суммы: сравниваем с ожидаемой суммы
    assert total_value == "$58.29", f"Ожидалось $58.29, а получено {total_value}"

    # 37. ДОПОЛНИТЕЛЬНЫЙ БЛОК (Finish): Нажимаем кнопку Finish
    finish_btn = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
    finish_btn.click()
    # 38. Убеждаемся что перешли на страницу .../checkout-complete.html
    wait.until(EC.url_contains("checkout-complete.html"))
    print(" ✅ Переход на финишную часть оформления заказа выполнен - ссылка соответствует ...//checkout-complete.html")

    # 39. Делаем скриншот страницы завершения
    driver.save_screenshot("screen_06K-img/test03_shop_finish.png")

    # 40. Нажимаем кнопку Generate PDF order
    pdf_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-pdf-order")))
    pdf_btn.click()
    print(" ⏳ Ожидаем скачивания PDF...")

    # ============================================================
    # БЛОК ОЖИДАНИЯ ПОЯВЛЕНИЯ PDF-ФАЙЛА В ПАПКЕ
    # ============================================================

    # 41. Ожидаем появления файла в папке PDF-order (ждём до 30 секунд)
    """ time - стандартная библиотека Python для работы со временем.
        Мы используем её, чтобы засеч время ожидания и делать паузы между проверками."""
    import time

    """ time.time() возвращает количество секунд, прошедших с 1 января 1970 года.
        Это нужно, чтобы засечь момент начала ожидания. """
    start_time = time.time()

    """ Переменная, в которую мы сохраним имя найденного PDF-файла.
        Изначально она равна None — файл ещё не найден. """
    pdf_file = None

    """ Цикл работает, пока прошло меньше 30 секунд с момента начала. 
        time.time() - start_time — сколько секунд уже прошло."""
    while time.time() - start_time < 30:

        """ 1.  os.listdir(download_dir) — получает список всех файлов в папке.
            2. for f in ... — перебираем каждый файл.
            3. if f.endswith(".pdf") — оставляем только те, чьё имя заканчивается на .pdf.
            4. [ ... ] — собираем результат в список (list comprehension)."""
        files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]

        # Если список files не пустой (то есть хотя бы один PDF-файл найден),
        if files:
            # берём первый найденный файл (обычно он единственный).
            pdf_file = files[0]
            # выходим из цикла — файл найден, ждать больше не нужно.
            break

        """ Если файл не найден, делаем паузу в 1 секунду и повторяем проверку.
            Это не sleep(30), а проверка каждую секунду — так мы не ждём лишнего времени,
            а реагируем сразу, как только файл появился."""
        time.sleep(1)  # Добавляем цикл ожидания

    """ assert — проверяет, что файл найден.
        pdf_file is not None — значит, в переменной есть имя файла.
        Если файл не найден за 30 секунд — тест падает с сообщением об ошибке."""
    assert pdf_file is not None, "PDF-файл так и не появился в папке PDF-order за 30 секунд"

    # Выводим имя файла в консоль для отчёта.
    print(f" ✅ PDF-файл {pdf_file} скачан в папку PDF-order")

    # 42. Выводим красивый итог в консоли
    print("\n" + "="*50)
    print("🛒  РЕЗУЛЬТАТ ТЕСТА (ПОКУПКА)")
    print("="*50)
    print(f" ✅ Товары добавлены: {', '.join(expected_names)}")
    print(f" ✅ Итоговая сумма: {total_value} (соответствует ожиданиям в $58.29)")
    print("="*50 + "\n")

    # 43. Закрываем браузер
    driver.quit()
