from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Задание:
# Откройте страницу https://httpbin.org/links/10.
# Найдите все ссылки на странице (тег <a>).
# Проверьте, что количество ссылок равно 9.
# Проверьте, что все ссылки отображаются на странице.
# Проверьте, что текст первой ссылки содержит "1".

