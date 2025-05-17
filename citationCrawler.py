from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from fake_useragent import UserAgent
from googleCrawler import make_request
from bs4 import BeautifulSoup
import time, re

options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'--user-agent={user_agent}')


test_url = "https://scholar.google.com/scholar?start=00&oi=bibs&hl=en&cites=8876951269706202931"

def generateCitationUrlsFinal(file='files/scholar.txt'):
    f = open(file, 'r', encoding='utf-8') 
    lines = f.readlines()
    filtered_lines = list(
        map(lambda line: line.rstrip('\n'),
        filter(lambda line: line.startswith('https://scholar.google.com/scholar?'), lines)))
    f.close()
    print(filtered_lines)
    
    # for link, index in enumerate(filtered_lines):
    #     response = make_request(link)
    #     if response.status_code != 200:
    #         return
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     results = soup.find_all('div', class_='gs_ab_mdw')
    #     results = results[1].get_text()
        
    #     results = re.search(r"about\s+(\d[\d,\.]*)\s+result", results, re.IGNORECASE).group(1)
    #     results_length = int(results)
    #     index = '00'
    #     f = open(f'files/journal_queries/{index}-{link.split("cites=")[1]}', 'w', encoding='utf-8')
    #     while(int(index) < results_length):
    #         f.write(f"{link}\n")
    #         link = link.replace(f'start={index}', f'start={int(index)+10}')
    #     f.close()
    
    

def getJournalsOnPage(url):   
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

        
generateCitationUrlsFinal()