# test_01_form.py

import os
from selenium import webdriver
from pages.form_page import FormPage
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    driver = webdriver.Edge()
    form_page = FormPage(driver)

    form_page.open()    # открываем браузер - метод открытия прописан в form_page.py

    # Список для вставки данных в поля которые тестируем
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
    form_page.submit()

    # Ждём появления элементов после отправки (id zip-code)
    from selenium.webdriver.common.by import By
    form_page.wait.until(EC.presence_of_element_located((By.ID, "zip-code")))

    assert form_page.is_field_red("zip-code"), "Zip-code должен быть красным!"
    for field_id in ["first-name", "last-name", "address", "city", "country", "e-mail", "phone", "company"]:
        assert form_page.is_field_green(field_id), f"Поле {field_id} должно быть зелёным!"

    print("\n" + "=" * 50)
    print("🔍 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ ФОРМЫ")
    print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    print(f"Если в классе есть '...-danger' → 🔴, если '...-success' → ✅")
    print("=" * 50)

    os.makedirs("screen_07-img", exist_ok=True)
    driver.save_screenshot("screen_07-img/test01_form.png")
    driver.quit()
