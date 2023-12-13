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
rootLogger = logging.getLogger()
logFormatter = logging.Formatter(
    fmt="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
fileHandler = logging.FileHandler(
    filename="selenium-test.log", mode='a', encoding='utf-8')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)
 
 
def initialize_browser():
    rootLogger.info('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    rootLogger.info(
        'Browser started successfully. Navigating to the demo page to login.')
    return driver
 
 
def login(user, password, driver):
    url = 'https://www.saucedemo.com/'
    driver.get(url)
    rootLogger.info("Succesfully navigated to " + url)
    driver.find_element(
        by=By.CSS_SELECTOR, value="input[id='user-name']").send_keys(user)
    driver.find_element(by=By.CSS_SELECTOR,
                        value="input[id='password']").send_keys(password)
    driver.find_element(by=By.CSS_SELECTOR,
                        value="input[id='login-button']").click()
 
    header = driver.find_element(
        by=By.CSS_SELECTOR, value="div[id='header_container'] > div[class='header_secondary_container'] > span.title").text
    assert "PRODUCTS" == header
    rootLogger.info("Succesfully loggeed to " + url + " with user " + user)
 
 
def add_items_to_shopping_cart(driver):
    for item, item_id in shopping_cart.items():
        css_selector = "button[id='add-to-cart-" + item_id + "']"
        driver.find_element(by=By.CSS_SELECTOR, value=css_selector).click()
        rootLogger.info(item + " has been added to a shopping cart.")
 
 
def remove_items_from_shopping_cart(driver):
    for item, item_id in shopping_cart.items():
        css_selector = "button[id='remove-" + item_id + "']"
        driver.find_element(by=By.CSS_SELECTOR, value=css_selector).click()
        rootLogger.info(item + " has been removed to a shopping cart.")
 
 
def test_if_items_are_in_shopping_cart(driver):
    shopping_cart_items = driver.find_element(
        by=By.CSS_SELECTOR, value="div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
    assert '6' in shopping_cart_items
    rootLogger.info("All products are successfully added to a cart. Totally found " +
                    shopping_cart_items + " items.")
 
 
def test_if_shoping_cart_is_empty(driver):
    try:
        driver.find_element(
            by=By.CSS_SELECTOR, value="div[id='shopping_cart_container'] > a > span.shopping_cart_badge").text
        cart_badge_not_found = False
    except:
        cart_badge_not_found = True
 
    assert cart_badge_not_found
    rootLogger.info("Shopping cart is empty.")
 
 
def main():
    driver = initialize_browser()
    login('standard_user', 'secret_sauce', driver)
    rootLogger.info("Check if shopping cart is empty...")
    test_if_shoping_cart_is_empty(driver)
    rootLogger.info("Adding items to shopping cart...")
    add_items_to_shopping_cart(driver)
    rootLogger.info("Check if items are succesfully added to a shopping cart")
    test_if_items_are_in_shopping_cart(driver)
    rootLogger.info("Removing objects from shopping cart...")
    remove_items_from_shopping_cart(driver)
    rootLogger.info("Check if shopping cart is empty...")
    test_if_shoping_cart_is_empty(driver)
    driver.quit()
    rootLogger.info("End of execution.")
 
 
if __name__ == '__main__':
    main()