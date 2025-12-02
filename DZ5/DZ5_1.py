import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_drag_and_drop_image_to_trash(browser):
    """
    Задание 2:
    https://www.globalsqa.com/demo-site/draganddrop/
    Перетащить первую фотографию в корзину и проверить:
    - в корзине 1 фото
    - в галерее осталось 3 фото
    """
    url = "https://www.globalsqa.com/demo-site/draganddrop/"
    browser.get(url)

    wait = WebDriverWait(browser, 20)

    # В этом демо нужный пример – вкладка "Photo Manager" и iframe внутри неё.
    # Сразу ждём iframe и ПЕРЕКЛЮЧАЕМСЯ в него.
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//div[@rel-title='Photo Manager']//iframe")
        )
    )

    # Ждём 4 картинки в галерее (это li внутри #gallery)
    gallery_items = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#gallery > li")
        )
    )
    assert len(gallery_items) == 4, "Ожидалось 4 фото в галерее перед перетаскиванием"

    first_photo = gallery_items[0]

    # Находим область корзины (droppable)
    trash = wait.until(
        EC.presence_of_element_located((By.ID, "trash"))
    )

    # Выполняем drag&drop – для этого демо стандартный метод обычно работает нормально
    actions = ActionChains(browser)
    actions.drag_and_drop(first_photo, trash).perform()

    # Ждём, пока в корзине появится хотя бы один элемент li
    wait.until(lambda drv: len(drv.find_elements(By.CSS_SELECTOR, "#trash li")) == 1)

    trash_photos = browser.find_elements(By.CSS_SELECTOR, "#trash li")
    gallery_photos = browser.find_elements(By.CSS_SELECTOR, "#gallery > li")

    assert len(trash_photos) == 1, "В корзине должно быть 1 фото после перетаскивания"
    assert len(gallery_photos) == 3, "В галерее должно остаться 3 фото после перетаскивания"
