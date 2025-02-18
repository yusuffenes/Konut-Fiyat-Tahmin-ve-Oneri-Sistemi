from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

def format_price(price):
    # Remove dots and convert to integer
    price = str(price)[0:-2]
    clean_price = price.replace('.', '')
    return int(clean_price)


def get_home_listings(selected_il, price_value):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--start-maximized')

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    driver.get('https://www.emlakjet.com/')

    # Wait for the element to be present and then send input data
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headlessui-tabs-panel-:r9:"]/div/div[2]/div/div/div/input'))
    )
    search_input.send_keys(f'{selected_il}')
    # Click the dropdown to open the price range options
    dropdown_button = driver.find_element(By.XPATH, '//*[@id="headlessui-listbox-button-:rh:"]')
    dropdown_button.click()

    # Calculate lower and upper bounds
    # Remove periods from the price string before calculation
    price_value = format_price(price_value)
    lower_bound = price_value - 500000
    upper_bound = price_value + 500000

    # Locate the first input element and set it to the lower bound
    first_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headlessui-listbox-options-:ri:"]/ul[1]/div[1]/div/div[1]/input'))
    )
    first_input.clear()
    first_input.send_keys(str(lower_bound))

    # Locate the second input element and set it to the upper bound
    second_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headlessui-listbox-options-:ri:"]/ul[2]/div[1]/div/div[1]/input'))
    )
    second_input.clear()
    second_input.send_keys(str(upper_bound))

    # Click the "Find" button to perform the search
    find_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-tabs-panel-:r9:"]/div/div[5]/div/button'))
    )
    find_button.click()

    i = 1
    data = []

    while i<=10:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="content-wrapper"]/div[1]/div[4]/div[2]/div[3]/div[{""+str(i)+""}]/div/a')))
        link = driver.find_element(By.XPATH, f'//*[@id="content-wrapper"]/div[1]/div[4]/div[2]/div[3]/div[{""+str(i)+""}]/div/a')
        driver.get(link.get_attribute('href'))
        detail_url = driver.current_url
        # Wait for the features list to load
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "ilan-hakkinda"))
        )
        
        try:
            ul = driver.find_element(By.XPATH, '//*[@id="ilan-hakkinda"]/div/div/ul')
            list_items = ul.find_elements(By.TAG_NAME, 'li')
            
            details = {}
            for item in list_items:
                try:
                    key = item.find_element(By.CLASS_NAME, 'styles_key__VqMhC').text
                    value = item.find_element(By.CLASS_NAME, 'styles_value__3QmL3').text
                    details[key] = value
                except NoSuchElementException:
                    continue

            # Extract the title
            title = driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/div[2]/div[1]/div/h1').text
            resim_url = driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/div[2]/div[2]/div[2]/img').get_attribute('src')
            fiyat = driver.find_element(By.XPATH, '//*[@id="genel-bakis"]/div[1]/div[1]/div[1]/div/span').text
            fiyat = int(fiyat.replace('.','').replace('TL',''))
            # Add the URL and title to the details
            details['url'] = detail_url
            details['title'] = title
            details['resim_url'] = resim_url
            details['price'] = fiyat
            


            data.append(details)

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        driver.execute_script("window.history.go(-1)")
        i += 1
        
    driver.quit()
    return data
