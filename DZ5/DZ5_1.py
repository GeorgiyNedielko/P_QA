import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def find_text_in_frames(driver, wait, target_text) -> bool:
    """
    Рекурсивно ищем target_text в текущем документе и во всех (вложенных) iframe.
    ВАЖНО: проверку is_displayed делаем сразу в том контексте, где нашли.
    """
    # 1) пробуем найти текст в текущем контексте (без переключения)
    try:
        elem = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(normalize-space(.), '{target_text}')]")
            )
        )
        return elem.is_displayed()
    except TimeoutException:
        pass

    # 2) если не нашли — идём по iframe (в этом контексте)
    frames = driver.find_elements(By.TAG_NAME, "iframe")

    for i in range(len(frames)):
        try:
            # каждый раз берём iframe заново (чтобы не словить StaleElementReference)
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[i])

            if find_text_in_frames(driver, wait, target_text):
                return True

            driver.switch_to.parent_frame()
        except StaleElementReferenceException:
            driver.switch_to.default_content()
            return find_text_in_frames(driver, wait, target_text)
        except Exception:
            # если вдруг конкретный фрейм “битый” — возвращаемся и идём дальше
            driver.switch_to.default_content()

    return False


def test_text_present_in_iframe(browser):
    url = "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
    browser.get(url)
    wait = WebDriverWait(browser, 20)

    target_text = "semper posuere integer et senectus justo curabitur."

    # ждём, что iframe вообще появились
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

    browser.switch_to.default_content()
    found = find_text_in_frames(browser, wait, target_text)

    assert found, "Не найден iframe (или вложенный iframe), содержащий искомый текст"
