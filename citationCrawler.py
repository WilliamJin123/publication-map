from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from fake_useragent import UserAgent
import time

options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'--user-agent={user_agent}')


test_url = "https://scholar.google.com/scholar?start=00&oi=bibs&hl=en&cites=8876951269706202931"
    
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get(test_url)
file = open("files/citations.txt", "w", encoding="utf-8")
while(True):
    try:
        journal_links = driver.find_elements(By.XPATH, '//a[@id]')
        for link in journal_links:
            if link.get_attribute('href') != None:
                file.write(f"{link.get_attribute('href')}\n")
        next_button = driver.find_element(By.XPATH, '//*[@id="gs_n"]/center/table/tbody/tr/td[-1]/a')
        next_button.click()
        time.sleep(1)
    except NoSuchElementException:
        print("Got to the end!")
        break    

        
