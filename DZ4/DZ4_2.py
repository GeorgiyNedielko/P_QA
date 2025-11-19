import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_loading_images(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

    # Ждём, пока третье изображение загрузится
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img:nth-of-type(3)"))
    )

    # Получаем alt
    alt_value = driver.find_element(By.CSS_SELECTOR, "img:nth-of-type(3)").get_attribute("alt")

    # Проверка
    assert alt_value == "award"

    # Сохранение скриншота
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_path = os.path.join(current_dir, "loading_images.png")
    driver.save_screenshot(screenshot_path)

    print(f"Скрин сохранён в: {screenshot_path}")
