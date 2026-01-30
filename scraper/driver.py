from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#
# options = Options()
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1080")
# options.binary_location = "/usr/bin/chromium"
#
#
# driver = webdriver.Chrome(
#     # service=Service(ChromeDriverManager().install()),
#     service=Service("/usr/bin/chromedriver"),
#     options=options
# )

options = Options()
options.add_argument("--headless=new")         # Headless режим
options.add_argument("--no-sandbox")           # Без песочницы, важно для Docker
options.add_argument("--disable-dev-shm-usage")# Использует /tmp вместо /dev/shm
options.add_argument("--disable-gpu")          # Иногда нужно для стабильности
options.add_argument("--window-size=1920,1080")

options.binary_location = "/usr/bin/chromium"

driver = webdriver.Chrome(
    service=Service("/usr/bin/chromedriver"),
    options=options
)