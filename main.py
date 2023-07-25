from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Driver setting not to auto close window
URL = "http://orteil.dashnet.org/experiments/cookie/"
chromedriver_autoinstaller.install()
chromedriver_path = "D:\Development\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)

# Get cookie to click on
cookie = driver.find_element(By.ID, "cookie")

# Get item upgrade ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
# print(item_ids)

#Get item upgrade ids
# item_names = []
# for item in item_ids:
#     item_name = item.split("buy")[1]
#     item_names.append(item_name)
# print(item_names)

five_sec = time.time() + 5
five_min = time.time() + 300

game_is_on = True

while game_is_on:
    cookie.click()

    if time.time() > five_sec:

        # Buy most expensive item within budget

        # Get list of item prices
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into integer price
        for price in all_prices:
            if price.text != " ":
                cost = int(price.text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break


