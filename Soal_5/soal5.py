from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get("https://astra.co.id/")
driver.maximize_window()
time.sleep(4)
driver.quit()