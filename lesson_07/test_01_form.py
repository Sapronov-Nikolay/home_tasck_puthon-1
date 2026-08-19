# test_01_form.py

import os, allure
from selenium import webdriver
from pages.form_page import FormPage
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Форма валидации")
@allure.story("Проверка подсветки полей после отправки")
@allure.title("Валидация формы: пустой Zip code → красный 🔴, остальные → зелёные ✅")
@allure.description("Заполняем форму, отправляем, проверяем цвета полей")
@allure.severity(allure.severity_level.NORMAL)
def test_form():
    with allure.step("Открыть браузер и страницу формы"):
        driver = webdriver.Edge()
        form_page = FormPage(driver)

        form_page.open()    # Открываем браузер - метод открытия прописан в form_page.py

    # Список для вставки данных в поля которые тестируем
    with allure.step("Заполнить форму данными"):
        data = {
            "first_name": "Николай",
            "last_name": "Сапронов",
            "address": "ул. Ленина, д.35, кв.15",
            "zip_code": "",
            "city": "Мурманск",
            "country": "Россия",
            "e-mail": "avindialit@list.ru",
            "phone": "89258906331",
            "job_position": "Программист",
            "company": "ООО 'ЭЛЕКТРО-ВЫСЯ'"
        }
        form_page.fill_form(data)

    with allure.step("Отправить форму"):
        form_page.submit()

        # Ждём появления элементов после отправки (id zip-code)
    with allure.step("Дождаться появления результата"):
        from selenium.webdriver.common.by import By
        form_page.wait.until(EC.presence_of_element_located((By.ID, "zip-code")))

    with allure.step("Проверить, что Zip code красный"):
        assert form_page.is_field_red("zip-code"), "Zip-code должен быть красным!"
        for field_id in ["first-name", "last-name", "address", "city", "country", "e-mail", "phone", "company"]:
            assert form_page.is_field_green(field_id), f"Поле {field_id} должно быть зелёным!"

    with allure.step("Вывести результат в консоль"):
        print("\n" + "=" * 50)
        print("🔍 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ ФОРМЫ")
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print(f"Если в классе есть '...-danger' → 🔴, если '...-success' → ✅")
        print("=" * 50)

    with allure.step("Сделать скриншот и закрыть браузер"):
        os.makedirs("screen_07-img", exist_ok=True)
        driver.save_screenshot("screen_07-img/test01_form.png")
        driver.quit()
