# pages/login_page.py
"""
Страница валидации главная www.saucedemo.com
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from .inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')

    def open(self):
        """Открываем страницу логина"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def login(self, username, password):
        """Выполнить вход и вернуть объект главной страницы"""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_url_contains("inventory.html")
        return InventoryPage(self.driver)
