import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    """Фикстура для Firefox"""
    options = webdriver.FirefoxOptions()

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_payment_methods_section(browser):
    browser.get("https://itcareerhub.de/ru")

    # Переход в раздел "Способы оплаты"
    browser.find_element(By.LINK_TEXT, "Способы оплаты").click()


    def find_payment_header(driver):
        headers = driver.find_elements(By.TAG_NAME, "h2")
        for h in headers:
            if "Способы оплаты" in h.text:
                return h
        return None

    payment_header = WebDriverWait(browser, 10).until(find_payment_header)

    # Скроллим к этой секции
    browser.execute_script("arguments[0].scrollIntoView(true);", payment_header)

    # Делаем скриншот этой части страницы (самого заголовка/секции)
    payment_header.screenshot("DZ2/payment_methods_section_firefox.png")
