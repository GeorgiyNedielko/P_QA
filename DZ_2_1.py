import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup_browser():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def close_cookies(driver):
    """Пытаемся закрыть cookie-баннер: сначала в основном DOM, потом во всех iframe."""
    wait = WebDriverWait(driver, 5)

    # 1. Попробовать найти кнопку напрямую в текущем контексте
    try:
        btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(normalize-space(.), 'Alle zulassen') "
                "or contains(normalize-space(.), 'Alle akzeptieren') "
                "or contains(normalize-space(.), 'Zustimmen')]"
            ))
        )
        btn.click()
        return
    except Exception:
        pass

    # 2. Если не нашли — пробуем во всех iframe
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            try:
                btn = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(normalize-space(.), 'Alle zulassen') "
                        "or contains(normalize-space(.), 'Alle akzeptieren') "
                        "or contains(normalize-space(.), 'Zustimmen')]"
                    ))
                )
                btn.click()
                driver.switch_to.default_content()
                return
            except Exception:
                driver.switch_to.default_content()
        except Exception:
            driver.switch_to.default_content()

    # если так и не нашли — просто выходим, дальше тест сам покажет, мешает ли баннер
    driver.switch_to.default_content()


def test_angebote_section(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, 20)

    # 1. Открываем сайт
    driver.get("https://www.mediamarkt.de")

    # 2. Закрываем cookie-баннер
    close_cookies(driver)

    # 3. Ждём ссылку ANGEBOTE в меню
    angebote_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[contains(translate(normalize-space(text()),"
            " 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ',"
            " 'abcdefghijklmnopqrstuvwxyzäöü'),"
            " 'angebote')]"
        ))
    )

    # 4. Кликаем по ANGEBOTE
    angebote_link.click()

    # 5. Ждём, пока на странице снова появится текст Angebote (страница загрузилась)
    wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(translate(normalize-space(text()),"
            " 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ',"
            " 'abcdefghijklmnopqrstuvwxyzäöü'),"
            " 'angebote')]"
        ))
    )

    # 6. Скрин всей страницы после перехода
    driver.save_screenshot("mediamarkt_angebote.png")
