import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_drag_and_drop_image_to_trash(browser):
    url = "https://www.globalsqa.com/demo-site/draganddrop/"
    browser.get(url)

    wait = WebDriverWait(browser, 20)

    # ---------- 1. Закрываем окно cookies ----------
    try:
        accept_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Соглашаюсь') or contains(text(),'Accept')]"))
        )
        accept_btn.click()
    except:
        pass  # Окно может не появиться — это нормально

    # ---------- 2. Переходим в iframe Photo Manager ----------
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//div[@rel-title='Photo Manager']//iframe")
        )
    )

    # ---------- 3. Ждем 4 фотографии ----------
    gallery_items = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li"))
    )
    assert len(gallery_items) == 4

    first_photo = gallery_items[0]

    # ---------- 4. Находим корзину ----------
    trash = wait.until(EC.presence_of_element_located((By.ID, "trash")))

    # ---------- 5. Выполняем "честный" drag&drop ----------
    actions = ActionChains(browser)
    actions.click_and_hold(first_photo).pause(0.2).move_to_element(trash).pause(0.4).release().perform()

    # ---------- 6. Проверяем, что фото появилось в корзине ----------
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#trash li")) == 1)



    trash_items = browser.find_elements(By.CSS_SELECTOR, "#trash li")
    gallery_after = browser.find_elements(By.CSS_SELECTOR, "#gallery li")

    assert len(trash_items) == 1, "В корзине должно быть 1 фото"
    assert len(gallery_after) == 3, "В галерее должно остаться 3 фото"
