from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_car_links(driver):
    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.address")
        )
    )

    return [
        el.get_attribute("href")
        for el in driver.find_elements(By.CSS_SELECTOR, "a.address")
    ]

def get_next_page(driver):
    try:
        next_btn = driver.find_element(
            By.CSS_SELECTOR,
            "a.page-link.js-next"
        )
        return next_btn.get_attribute("href")
    except:
        return None