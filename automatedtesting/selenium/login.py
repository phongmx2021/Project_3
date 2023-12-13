import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

shopping_cart = {
    "backpack": "sauce-labs-backpack",
    "bike light": "sauce-labs-bike-light",
    "gray T-shirt": "sauce-labs-bolt-t-shirt",
    "jacket": "sauce-labs-fleece-jacket",
    "onesie": "sauce-labs-onesie",
    "red T-shirt": "test.allthethings()-t-shirt-(red)"
}

def setup_logger():
    root_logger = logging.getLogger()
    log_formatter = logging.Formatter(
        fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(
        filename="selenium-test.log", mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)

def initialize_browser():
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.saucedemo.com/')
    return driver

def login(user, password, driver):
    url = 'https://www.saucedemo.com/'
    driver.get(url)
    root_logger.info("Successfully navigated to " + url)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='user-name']").send_keys(user)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='password']").send_keys(password)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='login-button']").click()
    header = driver.find_element_by_css_selector("span[class='title']").text
    assert "Products" == header
    root_logger.info("Successfully logged in to " + url + " with user " + user)

def add_items_to_shopping_cart(driver):
    for item, item_id in shopping_cart.items():
        css_selector = "button[id='add-to-cart-" + item_id + "']"
        driver.find_element(by=By.CSS_SELECTOR, value=css_selector).click()
        root_logger.info(item + " has been added to the shopping cart.")

def remove_items_from_shopping_cart(driver):
    for item, item_id in shopping_cart.items():
        css_selector = "button[id='remove-" + item_id + "']"
        driver.find_element(by=By.CSS_SELECTOR, value=css_selector).click()
        root_logger.info(item + " has been removed from the shopping cart.")

def test_if_items_are_in_shopping_cart(driver):
    shopping_cart_items = driver.find_element(
        by=By.CSS_SELECTOR, value="div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    assert '6' in shopping_cart_items
    root_logger.info("All products are successfully added to the cart. Found a total of " + shopping_cart_items + " items.")

def test_if_shopping_cart_is_empty(driver):
    try:
        driver.find_element(
            by=By.CSS_SELECTOR, value="div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
        cart_badge_not_found = False
    except:
        cart_badge_not_found = True

    assert cart_badge_not_found
    root_logger.info("The shopping cart is empty.")

def main():
    driver = initialize_browser()
    login('standard_user', 'secret_sauce', driver)
    root_logger.info("Checking if the shopping cart is empty...")
    test_if_shopping_cart_is_empty(driver)
    root_logger.info("Adding items to the shopping cart...")
    add_items_to_shopping_cart(driver)
    root_logger.info("Checking if items are successfully added to the shopping cart")
    test_if_items_are_in_shopping_cart(driver)
    root_logger.info("Removing items from the shopping cart...")
    remove_items_from_shopping_cart(driver)
    root_logger.info("Checking if the shopping cart is empty...")
    test_if_shopping_cart_is_empty(driver)
    driver.quit()
    root_logger.info("End of execution.")

if __name__ == '__main__':
    root_logger = logging.getLogger()
    setup_logger()
    main()