import scrapy
import re
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,TimeoutException
import logging




class CarPartSpider(scrapy.Spider):
    name = "car_part"
    allowed_domains = ["www.car-part.com"]
    start_urls = "https://www.car-part.com"
    listing_url = "https://kosiski.autopartsearch.com/catalog-6/vehicle"

    pause_for = 0
    
    headers = {
        'authority': 'www.car-part.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.car-part.com',
        'Referer': 'https://www.car-part.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    }

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls,
                              headers=self.headers,
                              callback=self.parse_home_page)
        
    
    def parse_home_page(self, response):
        print(self.start_urls)
        total_parts = 0

        driver = response.meta["driver"]

        selectyear = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@id="year"]'))))

        try:
            if WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//select[@id="year"]/option'))):

                YearValues = [option.get_attribute('value') for option in selectyear.options]

                for year in YearValues:
                    if year and year != "Select Year":  # Skip the placeholder option:
                        try:
                            selectyear.select_by_value(year)
                            sleep(self.pause_for)
                        except NoSuchElementException:
                            print(f"Option with value '{year}' not found in year dropdown.")
                            continue

                        selectmodel = Select(WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//select[@id="model"]'))))

                        try:
                            if WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, '//select[@id="model"]/option'))):
                                ModelValues = [option.get_attribute('value') for option in selectmodel.options]

                                for model in ModelValues:
                                    if model and model != "Select Make/Model":  # Skip the placeholder option
                                        try:
                                            selectmodel.select_by_value(model)
                                            sleep(self.pause_for)
                                            
                                        except NoSuchElementException:
                                            print(f"Option with value '{model}' not found in model dropdown.")
                                            continue

                                        selectParts = Select(WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.XPATH, '//select[@name="userPart"]'))))

                                        try:
                                            if WebDriverWait(driver, 5).until(
                                                    EC.presence_of_element_located(
                                                        (By.XPATH,
                                                        '//select[@name="userPart"]/option'))):
                                                partValues = [option.get_attribute('value') for option in
                                                            selectParts.options]

                                                for part in partValues:
                                                    print(part)
                                                    if part and part != "Select Part":
                                                        total_parts += 1
                                                        
                                                        try:
                                                            selectParts.select_by_value(part)
                                                            sleep(self.pause_for)
                                                            # sleep(1)

                                                            # Wait for the dropdown to be present and visible
                                                            selectarea = WebDriverWait(driver, 10).until(
                                                                EC.presence_of_element_located((By.XPATH, '//select[@id="Loc"]'))
                                                            )
                                                            # Create a Select object from the dropdown
                                                            select = Select(selectarea)

                                                            # Select the option by its visible text
                                                            select.select_by_visible_text('All Areas/Select an Area')
                                                            
                                                            selectsort = WebDriverWait(driver, 10).until(
                                                                EC.presence_of_element_located((By.XPATH, '//select[@name="userPreference"]'))
                                                            )
                                                            selects = Select(selectsort)
                                                            selects.select_by_visible_text('Year')
                                                            
                                                            print(total_parts, "|", model, "|", year, "|", part)

                                                            submit_btn = WebDriverWait(driver, 5).until(
                                                                EC.presence_of_element_located(
                                                                    (By.XPATH,
                                                                    '//input[@name="Search Car Part Inventory"]')))
                                                            submit_btn.click()
                                                            sleep(5)
                                                            
                                                            # Go back to the previous page to continue selecting other options
                                                            driver.back()
                                                            sleep(self.pause_for)
                                                            # Re-select the part for the next iteration
                                                            # selectParts = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//select[@name="userPart"]'))))
                                                
                                                                           
                                                        except:
                                                            pass
                                        except:
                                            pass
                        except:
                            pass
        except:
            pass
