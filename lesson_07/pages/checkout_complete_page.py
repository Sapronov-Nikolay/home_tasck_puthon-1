# pages/checkout_complete_page.py
"""
Страница завершения заказа (для кнопки Finish и скачивания PDF)
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    PDF_GENERATE_BUTTON = (By.ID, "generate-pdf-order")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def generate_pdf(self):
        """Нажать Generate PDF order"""
        self.click(self.PDF_GENERATE_BUTTON)

    def go_home(self):
        """Нажать Back Home."""
        self.click(self.BACK_HOME_BUTTON)
