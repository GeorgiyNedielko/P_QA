import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup_browser():
    options = webdriver.ChromeOptions()
    # если нужно — добавь сюда аргументы options.add_argument(...)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_payment_methods_section(setup_browser):
    driver = setup_browser
    driver.get("https://itcareerhub.de/ru")

    # Попробуем закрыть cookie-баннер, если он есть
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Подтвердить')]"))
        ).click()
    except Exception:
        pass  # если не нашли — просто идём дальше

    # Переход к разделу "Способы оплаты"
    driver.find_element(By.LINK_TEXT, "Способы оплаты").click()

    # Ждём появления блока "Способы оплаты и рассрочки"
    payment_section = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Способы оплаты и рассрочки')]")
        )
    )

    # Скроллим к блоку (на всякий случай) и делаем скриншот
    driver.execute_script("arguments[0].scrollIntoView(true);", payment_section)
    payment_section.screenshot("payment_methods_section.png")
