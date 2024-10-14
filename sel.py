from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time


def get_driver():
    # initiate web options
    options = Options()

    # fullsize window
    options.add_argument("--window-size=1920,1080")

    # disable images
    # options.add_argument("--blink-settings=imagesEnabled=false")

    # ignore certificate errors
    options.add_argument("--ignore-certificate-errors")

    # disable notifications
    options.add_argument("--disable-notifications")

    # disable pop-up
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

    # headless mode
    # chrome_options.add_argument("--headless")
    

    driver = webdriver.Chrome(options=options)
    return driver

def get_image(driver, url):
    driver.get(url)

    buttons = driver.find_elements(By.CSS_SELECTOR, "button.css-w2e02c")

    for button in buttons:
        button.click()
        time.sleep(3)
        img_element = driver.find_element(By.CSS_SELECTOR, "img[data-testid='PDPMainImage']")
        img_url = img_element.get_attribute("src")
        print(img_url)


"""
Challenge: Download all image without re-downloading from start
"""


if __name__ == "__main__":
    url = "https://www.tokopedia.com/hawman/tas-micro-size-hawman-transparant?extParam=src%3Dshop%26whid%3D2496341"

    driver = get_driver()
    get_image(driver, url)
    


