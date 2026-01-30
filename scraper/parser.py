import re
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def parse_phone(wait):

    phone_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.size-large.conversion")
        )
    )
    phone_button.click()

    popup = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.popup-inner")
        )
    )

    phone = popup.find_element(
        By.CSS_SELECTOR,
        "span.common-text.ws-pre-wrap.action"
    ).text

    phone = (
        phone.replace("(", "")
             .replace(")", "")
             .replace(" ", "")
             .replace("-", "")
    )
    return phone

def parse_title(wait):
    return wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.common-text.ws-pre-wrap.titleL")
        )
    ).text


def parse_price_usd(wait):
    price = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "strong.common-text.ws-pre-wrap.titleL")
        )
    ).text

    return int(re.sub(r"\D", "", price))

def parse_odometer(wait):
    info_block = wait.until(
        EC.presence_of_element_located(
            (By.ID, "basicInfoTableMainInfo")
        )
    )

    spans = info_block.find_elements(By.CSS_SELECTOR, "span.common-text.ws-pre-wrap.body")

    odometer = None
    for span in spans:
        text = span.text.strip()
        if "тис" in text:
            odometer = int(float(text.split()[0]) * 1000)
            break

    return odometer

def parse_username(wait):
    return wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.common-text.ws-pre-wrap.titleM")
        )
    ).text

def parse_image_url(wait):
    picture = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "picture")
        )
    )
    img = picture.find_element(By.TAG_NAME, "img")
    return img.get_attribute("src")

def parse_images_count(wait):
    img = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.common-badge.alpha.medium")
        )
    )
    img_num = img.find_elements(By.TAG_NAME, "span")
    return img_num[1].text

def parse_car_number(driver):
    car_number = driver.execute_script("""
    let el = document.querySelector('div.car-number.ua span.common-text.ws-pre-wrap.body');
    return el ? el.innerText.replace(/\s+/g, '') : null;
    """)
    return car_number


def parse_car_vin(driver):
    vin = driver.execute_script("""
    let el = document.querySelector('div.badge-template span.common-text.ws-pre-wrap.badge');
    return el ? el.innerText.replace(/\s+/g, '') : null;
    """)
    return vin

def parse_car_page(driver, url):
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    phone = parse_phone(wait)
    title = parse_title(wait)
    price_usd = parse_price_usd(wait)
    odometer = parse_odometer(wait)
    username = parse_username(wait)
    image_url = parse_image_url(wait)
    images_count =parse_images_count(wait)
    car_number = parse_car_number(driver)
    car_vin = parse_car_vin(driver)

    return {
        "url": url,
        "title": title,
        "price_usd": price_usd,
        "odometer": odometer,
        "username": username,
        "phone_number": phone,
        "image_url": image_url,
        "images_count": images_count,
        "car_number": car_number,
        "car_vin": car_vin,
        "datetime_found": datetime.utcnow(),
    }