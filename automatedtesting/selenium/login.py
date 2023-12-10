# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import datetime
import time

def timestamp():
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (ts + '\t')

# Start the browser and login with standard_user
def login(user, password):
    print(timestamp() + 'Starting the browser...')
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    print(timestamp() + 'Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    # login
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    print(timestamp() + 'Get element user name oke.')
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    print(timestamp() + 'Get element password oke.')
    driver.find_element_by_id("login-button").click()
    print(timestamp() + 'Click login oke')
    time.sleep(30) 
    print(timestamp() + 'Doi 30s xong')
    product_label = driver.find_element_by_css_selector("span[class='title']").text
    print(timestamp() + 'Get product label oke')
    assert "Products" in product_label
    print(timestamp() + 'Login with username {:s} and password {:s} successfully.'.format(user, password))
    return driver

def add_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"  # Get the URL of the product
        print(timestamp() + 'Add item item_'+ str(i) + '_title_link')
        driver.find_element_by_css_selector(element).click()  # Click the URL
        print(timestamp() + 'Add element'+ element)
        driver.find_element_by_css_selector("button.btn_primary.btn_inventory").click()  # Add the product to the cart
        print(timestamp() + 'click button add'+ element)
        print(timestamp() + 'add product number '+ str(i))
        # xpath_expression = "//a[@id='item_"+str(i)+"_title_link']//div[@class='inventory_item_name ']"
        # print(timestamp() + 'xpath:'+ xpath_expression)
        # inventory_item_name = driver.find_element(By.XPATH, xpath_expression)
        product = driver.find_element_by_css_selector("div[class='inventory_details_name ']").text 
        print(timestamp() + product + " added to shopping cart.")  # Display message saying which product was added
        driver.find_element_by_css_selector("button.inventory_details_back_button").click()  # Click the Back button
    print(timestamp() + '{:d} items are all added to shopping cart successfully.'.format(n_items))

def remove_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element_by_css_selector(element).click()
        driver.find_element_by_css_selector("button.btn_secondary.btn_inventory").click()
        product = driver.find_element_by_css_selector("div[class='inventory_item_name ']").text
        print(timestamp() + product + " removed from shopping cart.")  # Display message saying which product was added
        driver.find_element_by_css_selector("button.inventory_details_back_button").click()
    print(timestamp() + '{:d} items are all removed from shopping cart successfully.'.format(n_items))


if __name__ == "__main__":
    N_ITEMS = 6
    TEST_USERNAME = 'standard_user'
    TEST_PASSWORD = 'secret_sauce'
    driver = login(TEST_USERNAME, TEST_PASSWORD)
    add_cart(driver, N_ITEMS)
    remove_cart(driver, N_ITEMS)
    print(timestamp() + 'Selenium tests are all successfully completed!')