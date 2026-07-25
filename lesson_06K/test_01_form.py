import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    # 1. Запускаем браузер Edge
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)

    # 2. Открываем заданную в задании страницу и разворачиваем на весь экран
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    driver.maximize_window()

    # 3. Заполняем форму: и ждём пока она полностью прогрузится. Загрузится первая форма → загрузятся и остальные.
    # Для остальных полей используем driver.find_element (они уже точно есть)
    # 3.1 Заполняем поле Имя
    first_name = wait.until(EC.presence_of_element_located((By.NAME, "first-name")))
    first_name.send_keys("Николай")

    # 3.2 Заполняем поле Фамилия
    last_name = driver.find_element(By.NAME, "last-name")
    last_name.send_keys("Сапронов")

    # 3.3 Заполняем поле адрес
    address = driver.find_element(By.NAME, "address")
    address.send_keys("ул. Ленина, д.35, кв.15")

    # 3.4 Заполняем индекс (по условию не заполняем)
    zip_code = driver.find_element(By.NAME, "zip-code")
    zip_code.send_keys("")

    # 3.5 Заполняем город
    city = driver.find_element(By.NAME, "city")
    city.send_keys("Мурманск")

    # 3.6 Заполняем страну
    country = driver.find_element(By.NAME, "country")
    country.send_keys("Россия")

    # 3.7 Указываем эмейл
    email = driver.find_element(By.NAME, "e-mail")
    email.send_keys("avindialit@list.ru")

    # 3.8 Указываем телефон
    phone = driver.find_element(By.NAME, "phone")
    phone.send_keys("89036896235")

    # 3.9 Заполняем поле работа
    job = driver.find_element(By.NAME, "job-position")
    job.send_keys("Программист")

    # 3.10 Указываем место работы.
    company = driver.find_element(By.NAME, "company")
    company.send_keys("ООО 'ЭЛЕКТРО-ВАСЯ'")

    # 4. Нажмём на кнопку SUBMIT
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()


    # 5. Говорим тесту какие поля должны быть зелёными, а какие красные
    # Создаём словарь.
    expected_fields = {
        "first-name": "success",
        "last-name": "success",
        "address": "success",
        "zip-code": "danger",   # это поле должно быть красным
        "city": "success",
        "country": "success",
        "e-mail": "success",
        "phone": "success",
        "job-position": "success",
        "company": "success"
    }

    # 6. Ждём, пока все поля появятся после отправки формы
    wait.until(EC.presence_of_element_located((By.ID, "zip-code")))

    # 7. Оформляем вывод в консоль
    print("\n" + "="*50)
    print("🔍 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ ФОРМЫ")
    print("="*50)

    # 8. Флаг про то, что проверка прошла
    all_passed = True

    # 9. Прогоняем элементы формы через for
    for field_id, expected in expected_fields.items():
        # Находим элемент по ID
        field = driver.find_element(By.ID, field_id)
        # Получаем класс
        field_class = field.get_attribute("class")

        # Определяем отдельный статус по классу
        if "alert-danger" in field_class:
            actual = "danger"   # RED
            emoji = "🔴 "
        elif "alert-success" in field_class:
            actual = "success"  # GREEN
            emoji = " ✅"
        else:
            emoji = " ⚠️"    # class не найден

        # Сравниваем ожидаемый результат
        if actual == expected:
            print(f" {emoji}  {field_id:20} → {actual.upper()} (ожидалось: {expected.upper()})")
        else:
            print(f" {emoji}  {field_id:20} → {actual.upper()}  (ожидалось: {expected.upper()})")
            all_passed = False # В случае ошибки

    # 10. ОФОРМЛЯЕМ ВЫВОД В КОНСОЛИ
    print("="*50)

    # 10.1. # Финальная проверка: если хотя бы одно поле не совпало — тест упадёт
    assert all_passed, "Поля с неверным статусом валидации"
    print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    print(f"Если в классе есть '...-danger' → 🔴, если '...-success' → ✅")
    print("="*50)

    # 11. Делаем скриншот страницы в папку "screen_06K-img" после всех проверок
    os.makedirs("screen_06K-img", exist_ok=True)
    driver.save_screenshot("screen_06K-img/test01_form.png")

    # 12. Выходим
    driver.quit()
