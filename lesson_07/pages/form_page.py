# pages/form_page.py
"""
Класс для страницы с формой валидации (первый тест)
URL: https://bonigarsia.dev/selenium-webdriver-java/data-types.html
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class FormPage(BasePage):
    # Локаторы полей (определяем по name, тфк как до отправки это input`ы)
    FIRST_NAME = (By.NAME, 'first-name')
    LAST_NAME = (By.NAME, 'last-name')
    ADDRESS = (By.NAME, 'address')
    ZIP_CODE = (By.NAME, 'zip-code')
    CITY = (By.NAME, 'city')
    COUNTRY = (By.NAME, 'country')
    EMAIL = (By.NAME, 'e-mail')
    PHONE = (By.NAME, 'phone')
    JOB = (By.NAME, 'job-position')
    COMPANY = (By.NAME, 'company')
    SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit"]')

    def open(self):
        """Открыт страницу формы"""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
        self.driver.maximize_window()

    def fill_form(self, data):
        """Заполняем поля данными"""
        self.send_keys(self.FIRST_NAME, data["first_name"])
        self.send_keys(self.LAST_NAME, data["last_name"])
        self.send_keys(self.ADDRESS, data["address"])
        self.send_keys(self.ZIP_CODE, data["zip_code"])
        self.send_keys(self.CITY, data["city"])
        self.send_keys(self.COUNTRY, data["country"])
        self.send_keys(self.EMAIL, data["e-mail"])
        self.send_keys(self.PHONE, data["phone"])
        self.send_keys(self.JOB, data["job_position"])
        self.send_keys(self.COMPANY, data["company"])

    def submit(self):
        """Нажать кнопку Submit."""
        self.click(self.SUBMIT_BUTTON)

    def get_field_class(self, field_id):
        """После кнопки submit поля из <div> на id. Возвращает значение класса."""
        locator = (By.ID, field_id)
        # Пока нет метода get_attribute до написания 3-его теста используем driver напрямую
        return self.driver.find_element(*locator).get_attribute("class")

    def is_field_red(self, field_id):
        """Проверить, что поле красное (содержит alter-danger)."""
        return "alert-danger" in self.get_field_class(field_id)

    def is_field_green(self, field_id):
        """Проверить, что поле зелёное (содержит alter-success)."""
        return "alert-success" in self.get_field_class(field_id)
