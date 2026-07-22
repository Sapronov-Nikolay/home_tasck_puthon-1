# pages/base_page.py
"""
Базовый класс для всех страниц.
Содержит общие методы, которые используются в любом PageObject.
Это позволяет не дублировать код в каждом классе страницы.
Для третьего теста появляются scroll_to и get_attribute -
"""
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        """Ожидание видимости элемента и его вывод."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Ожидать кликабельности элемента и кликнуть по нему"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        """Очистить поле и ввести текст"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Получить видимый текст элемента"""
        return self.find_element(locator).text

    def get_attribute(self, locator, attr):
        """Получение значения для результата итогов"""
        return self.find_element(locator).get_attribute(attr)

    def scroll_to(self, locator):
        """Прокрутить страницу до элемента итогов"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def wait_for_url_contains(self, text):
        """Ожидание, пока URL не начнёт содержать указанный текст. Что означает - переход на другую страницу"""
        self.wait.until(EC.url_contains(text))
