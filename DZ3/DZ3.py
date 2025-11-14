import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://itcareerhub.de/ru"


@pytest.fixture
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)  # немного ждём элементы
    yield driver
    driver.quit()

def close_cookies(driver):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if "Подтвердить" in btn.text:
            btn.click()
            break

def test_logo_is_displayer(driver):
    driver.get((BASE_URL))
    close_cookies(driver)
    logo = driver.find_element(By.TAG_NAME, "img")
    assert  logo.is_displayed(), "Логотипа нет"

def test_menu_links_are_displayed(driver):
    driver.get(BASE_URL)
    close_cookies(driver)

    assert driver.find_element(By.LINK_TEXT, "Программы").is_displayed()
    assert driver.find_element(By.LINK_TEXT, "Способы оплаты").is_displayed()
    assert driver.find_element(By.LINK_TEXT, "О нас").is_displayed()
    assert driver.find_element(By.LINK_TEXT, "Отзывы").is_displayed()
    assert driver.find_element(By.LINK_TEXT, "Блог").is_displayed()

def test_language_switch_buttons_are_displayed(driver):
    driver.get(BASE_URL)
    close_cookies(driver)

    assert driver.find_element(By.LINK_TEXT, "ru").is_displayed()
    assert driver.find_element(By.LINK_TEXT, "de").is_displayed()

def test_phone_icon_and_text_is_displayed(driver):
    driver.get(BASE_URL)
    close_cookies(driver)

    # Иконка / ссылка с телефонной трубкой
    phone_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
    assert phone_link.is_displayed(), "Иконка телефона не отображается"
    driver.execute_script("arguments[0].setAttribute('href', '#')", phone_link)
    phone_link.click()

    driver.get("https://itcareerhub.de/ru/schulgebuhren")

    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"

    # Без XPATH: просто проверяем, что текст есть в HTML страницы
    page_source = driver.page_source
    assert expected_text in page_source, "Нужный текст не отображается на странице"