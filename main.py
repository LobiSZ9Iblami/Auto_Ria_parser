import os
from dotenv import load_dotenv

from scraper.parser import parse_car_page
from scraper.driver import driver
from scraper.car_links import get_car_links, get_next_page
from db.db import init_db, save_car, wait_for_db


load_dotenv()


def main():
    driver.get(os.getenv("URL"))
    wait_for_db()
    init_db()
    while True:
        car_links = get_car_links(driver)

        for link in car_links:
            car_data = parse_car_page(driver, link)
            save_car(car_data)
        next_page = get_next_page(driver)
        if not next_page:
            break

        driver.get(next_page)

    driver.quit()

if __name__ == "__main__":
    main()