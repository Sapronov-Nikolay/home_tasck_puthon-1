# pages/cart_page.py
"""
Страница корзины.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from .checkout_step_one_page import CheckoutStepOnePage

class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def get_item_name(self):
        """Количество товаров в корзине - циферка на ярлыке корзины"""
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_item_names(self):
        """Список названий товаров положенных в корзину"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        names = []
        for item in items:
            name_elem = item.find_element(*self.ITEM_NAME)
            names.append(name_elem.text)
        return names

    def proceed_to_checkout(self):
        """Нажать Checkout"""
        self.click(self.CHECKOUT_BUTTON)
        # Проверяем, что часть адресной строка начала иметь указанный текст (часть)
        self.wait_for_url_contains("checkout-step-one.html")
        return CheckoutStepOnePage(self.driver)