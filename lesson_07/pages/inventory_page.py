# pages/inventory_page.py

"""
Главная страница магазина (списки товаров)
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from .cart_page import CartPage

class InventoryPage(BasePage):
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    # Локатор собирающий данные для определения состояния кнопки до добавления товара в корзину
    @staticmethod
    @allure.step("Определяем состояние кнопки до добавления товаров в корзину 'Add to Cart'")
    def get_add_button_locator(product_name):
        return (By.ID, f"add-to-cart-sauce-labs-{product_name}")

    # Локатор собирающий данные для определения состояния кнопки после добавления товара в корзину
    @staticmethod
    @allure.step("Определяем состояние кнопки после добавления товаров в корзину 'Remove'")
    def get_remove_button_locator(product_name):
        return (By.ID, f"remove-sauce-labs-{product_name}")

    @allure.step("Добавить товар '{product_name}' в корзину")
    def add_item_to_cart(self, product_name):
        """Нажать на Add to cart и проверить, что кнопка стала Remove"""
        # 1. Кликаем Add to cart
        self.click(self.get_add_button_locator(product_name))
        # 2. Проверяем, что кнопка сменила текст на "Remove"
        remove_btn = self.get_remove_button_locator(product_name)
        self.wait.until(EC.visibility_of_element_located(remove_btn))
        assert self.get_text(remove_btn) == "Remove", f"Кнопка для {product_name} не стала 'Remove'"

    @allure.step("Получить количество товаров в корзине")
    def get_cart_count(self):
        """Возвращаем количество товара, отображаемое на значке корзины."""
        return int(self.get_text(self.CART_BADGE))

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """Переходим в корзину"""
        self.click(self.CART_LINK)
        self.wait_for_url_contains("cart.html")
        return CartPage(self.driver)
