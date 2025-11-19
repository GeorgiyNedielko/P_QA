from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os

# Определяем путь текущей папки
current_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_path = os.path.join(current_dir, "screenshot.png")

driver = webdriver.Chrome()
driver.implicitly_wait(10)

try:
    driver.get("http://uitestingplayground.com/textinput")

    driver.find_element(By.ID, "newButtonName").send_keys("ITCH")
    driver.find_element(By.ID, "updatingButton").click()
    sleep(1)

    # Сохраняем скриншот в ту же папку
    driver.save_screenshot(screenshot_path)
    print(f"Скрин сохранён: {screenshot_path}")

finally:
    driver.quit()
