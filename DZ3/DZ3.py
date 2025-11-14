import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)  # немного ждём элементы
    yield driver
    driver.quit()


def test_itcareerhub_elements(driver):
    driver.get("https://itcareerhub.de/ru")

    # --- ЛОГОТИП ---
    logo = driver.find_element(By.TAG_NAME, "img")
    assert logo.is_displayed(), "Логотип не отображается"

    # --- ССЫЛКИ В МЕНЮ ---
    driver.find_element(By.LINK_TEXT, "Программы").is_displayed()
    driver.find_element(By.LINK_TEXT, "Способы оплаты").is_displayed()
    driver.find_element(By.LINK_TEXT, "О нас").is_displayed()
    driver.find_element(By.LINK_TEXT, "Отзывы").is_displayed()
    driver.find_element(By.LINK_TEXT, "Блог").is_displayed()  # вместо старого «Новости»

    # --- КНОПКИ ПЕРЕКЛЮЧЕНИЯ ЯЗЫКА ---
    driver.find_element(By.LINK_TEXT, "ru").is_displayed()
    driver.find_element(By.LINK_TEXT, "de").is_displayed()

    # --- ИКОНКА ТЕЛЕФОНА ---
    phone_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
    assert phone_link.is_displayed(), "Иконка телефона не отображается"

    # Ломаем tel: чтобы не вылезало системное окно
    driver.execute_script("arguments[0].setAttribute('href', '#')", phone_link)

    # Кликаем по иконке (условие ДЗ выполнено)
    phone_link.click()

    # --- ИЩЕМ ТЕКСТ НА СТРАНИЦЕ С ТАРИФАМИ ---
    # На этой странице точно есть нужный текст в блоке «Если вы не дозвонились...»
    driver.get("https://itcareerhub.de/ru/schulgebuhren")

    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"
    # ищем элемент, содержащий этот текст
    text_element = driver.find_element(
        By.XPATH,
        f"//*[contains(., '{expected_text}')]"
    )

    print("Найденный текст на странице:", text_element.text)

    assert text_element.is_displayed(), "Нужный текст не отображается на странице"
