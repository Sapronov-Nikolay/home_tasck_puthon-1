# pages/checkout_step_one_page.py
"""
Страница оформления заказа (шаг 1) - ввод данных покупателем.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from .checkout_step_two_page import CheckoutStepTwoPage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def fill_customer_info(self, first_name, last_name, postal_code):
        """Заполнение формы и нажатие кнопки Continue."""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)
        # Ждём когда ссылка начнёт содержать указанный текст
        self.wait_for_url_contains("checkout-step-two.html")
        return CheckoutStepTwoPage(self.driver)
