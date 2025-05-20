from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   
from fake_useragent import UserAgent
from googleCrawler import make_request, extractListfromFile
from bs4 import BeautifulSoup
import time, re

options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'--user-agent={user_agent}')

test_url = "https://scholar.google.com/scholar?start=00&oi=bibs&hl=en&cites=8876951269706202931"
CURREAD = 24
URL_LIST = ['javascript:void(0)', 'https://scholar.google.com/', 'https://accounts.google.com/',  ]


def generateCitationUrlsFinal(file='files/scholar.txt'):
    f = open(file, 'r', encoding='utf-8') 
    lines = f.readlines()
    filtered_lines = list(
        map(lambda line: line.rstrip('\n'),
        filter(lambda line: line.startswith('https://scholar.google.com/scholar?'), lines)))
    f.close()
    
    for i, link in enumerate(filtered_lines):
        if i <= CURREAD:
            continue    
        response = make_request(link)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='gs_ab_mdw')
        results = results[1].get_text()
        
        results = re.search(r"about\s+(\d[\d,\.]*)\s+result", results, re.IGNORECASE).group(1)
        results_length = int(results)
        print(results_length)
        index = '00'
        f = open(f'files/journal_queries/{i}-{link.split("cites=")[1]}', 'w', encoding='utf-8')
        while(int(index) < results_length):
            f.write(f"{link}\n")
            link = link.replace(f'start={index}', f'start={int(index)+10}')
            index = str(int(index)+10)
        f.close()
    
def captchaCheck(driver):
    while(True):
        if "recaptcha" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
            print("\nCaptcha detected!")
            driver.implicitly_wait(10)
            time.sleep(3)
        else:
            break

def getJournalsOnPage(url):   
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    
    file = open(f"files/citations/{url.split('cites=')[1]}.txt", "w", encoding="utf-8")
    # captchaCheck(driver)
    # numresults = driver.find_element(By.XPATH, '//*[@id="gs_ab_md"]/div').text
    # numresults = re.search(r"about\s+(\d[\d,\.]*)\s+result", numresults, re.IGNORECASE).group(1)
    # for i in range (int(numresults)//10):
    
    def getLinks():
        captchaCheck(driver)
        journal_links = driver.find_elements(By.XPATH, '//a[@id]')
        for link in journal_links:
            if link.get_attribute('href') != None and not any(link.get_attribute('href').startswith(url) for url in URL_LIST):
                print(link.get_attribute('href'))
                file.write(f"{link.get_attribute('href')}\n")        
            
    while(True):
        getLinks()
        try:
            next_button = driver.find_element(By.XPATH, '//*[@id="gs_nm"]/button[2]')
            print(next_button.text)
            if not next_button.is_enabled():
                print("No more pages!")
                break
            next_button.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            print('using link')
            
            next_pages = driver.find_elements(By.XPATH, '//*[@id="gs_n"]/center/table/tbody/tr/td/a')
            next_link = next_pages[-1]
            try:
                span = next_link.find_element(By.CLASS_NAME, 'gs_ico.gs_ico_nav_next')
                next_link.click()
                time.sleep(1)
            except NoSuchElementException:
                print('No more pages!')
                break
    driver.close()

def appendToLine(index, filepath="files/scholar.txt", text="ignore:"):
    with open(filepath, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if index == i:
                lines[i] = f'{text}' + lines[i]
        file.seek(0)
        file.writelines(lines)
        file.truncate()      

if __name__ == "__main__":
   
    # generateCitationUrlsFinal()
    
    googleLinks = extractListfromFile()
    for i, link in enumerate(googleLinks):
        if link.startswith("ignore:"):
            continue
        print(f'Processing {i+1}/{len(googleLinks)}')
        getJournalsOnPage(link)
        appendToLine(i)
    
    # appendToLine(2)
    
    # getJournalsOnPage('https://scholar.google.com/scholar?start=00&oi=bibs&hl=en&cites=16913045085278989081')