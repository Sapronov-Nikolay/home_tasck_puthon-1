# page/calculator_page.py
"""
Класс для страницы медленного калькулятора.
Использует методы из BasePage: click, send_keys, get_text.
Добавляет свой метод wait_for_result, который использует self.wait.wait напрямую
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class CalculatorPage(BasePage):
    DELAY_INPUT = (By.ID, "delay")
    SCREEN = (By.CLASS_NAME, "screen")

    @staticmethod
    def get_button_locator(text):
        """Вернуть локатор для кнопки по её тексту (7, +, 8, =)."""
        return (By.XPATH, f"//span[text()='{text}']")

    def open(self):
        """Открыть страницу калькулятора"""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.driver.maximize_window()
        # Дожидаемся появления поля задержки, чтобы убедиться, что страница загружена
        self.wait.until(EC.visibility_of_element_located(self.DELAY_INPUT))

    def set_delay(self, seconds):
        """Установить задержку в поле #delay"""
        self.send_keys(self.DELAY_INPUT, str(seconds))

    def click_button(self, text):
        """Нажать кнопку с заданным текстом"""
        self.click(self.get_button_locator(text))

    def get_result(self):
        """Получить текст из экрана калькулятора (div.screen)"""
        return self.get_text(self.SCREEN)

    def wait_for_result(self, expected_text, timeout=50):
        """Ожидать результат ожидаемого текста в экране (таймаут 50 сек)"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.text_to_be_present_in_element(self.SCREEN, expected_text))