# pages/checkout_step_two_page.py
"""
Страница оформления заказа (шаг 2) - итоговая сумма.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish") # Для дополнительного блока - для нажатия кнопки finish

    def get_total(self):
        """Получить итоговую сумму (Total) и вернуть как строку без части текста 'Total: '."""
        self.scroll_to(self.TOTAL_LABEL)   # прокручиваем до суммы
        total_text = self.get_text(self.TOTAL_LABEL)
        return total_text.replace("Total: ", "").strip()

    def finish(self):
        """Нажать Finish и перейти на страницу завершения."""
        self.click(self.FINISH_BUTTON)
        self.wait_for_url_contains("checkout-complete.html")
        from .checkout_complete_page import CheckoutCompletePage
        return CheckoutCompletePage(self.driver)