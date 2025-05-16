# crawl google citations, look into journal articles, look into authors, fetch countries, store in csv file
import requests, time
from bs4 import BeautifulSoup
import re 
import random
import time


prof_urls = [
    "https://scholar.google.com/citations?user=9T0HBb0AAAAJ&hl=en&cstart=0&pagesize=100",
    "https://scholar.google.com/citations?user=9T0HBb0AAAAJ&hl=en&cstart=100&pagesize=200",
    "https://scholar.google.com/citations?user=9T0HBb0AAAAJ&hl=en&cstart=200&pagesize=300",]  

alternate_headers = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.2210.144"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.63.165 Chrome/122.0.6261.94 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:124.0) Gecko/20100101 Firefox/124.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Mobile Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.170 Mobile Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS_20160321T151123; rv:11.0) like Gecko" # Internet Explorer 11
    },
    {
        "User-Agent": "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18" # Opera 12
    },
]

def loadProxies(filepath="files/proxies_list.txt"):
    with open(filepath, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

proxy_list = loadProxies()

def make_request(url):
    headers = headers = random.choice(alternate_headers)
    # proxy = random.choice(proxy_list)
    # proxies = {
    #     "http": f"http://{proxy}",  # Or "http://username:password@ip:port"
    #     "https": f"https://{proxy}", # Or "https://username:password@ip:port"
    # }
    # print(proxies)
    time.sleep(random.uniform(0.6,1.5))
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.text)
    return response




def getScholarData(urls):
    
    
    file = open("files/scholar.txt", "w", encoding="utf-8")
    for url in urls:
        response = make_request(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        link_tags = soup.find_all('a', class_=['gsc_a_ac', 'gs_ibl'])
        for link in link_tags:
            file.write(f"{link['href'].replace('?', '?start=00&')}\n") 
    file.close()

# getScholarData(prof_urls)

def extractListfromFile(file='files/scholar.txt'):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        filtered_lines = list(
            map(lambda line: line.rstrip('\n'),
            filter(lambda line: line.startswith('https://scholar.google.com/scholar?'), lines)))
        return filtered_lines




def getCitationUrls(paper):
    
    response = make_request(paper)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='gs_ab_mdw')
    results = results[1].get_text()
    
    results = re.search(r"about\s+(\d[\d,\.]*)\s+result", results, re.IGNORECASE).group(1)
    results_length = int(results)
    print(results_length)
    index = '00'
    file = open("files/citations.txt", "w", encoding="utf-8")

    while(int(index) < results_length):
        citations = make_request(paper)
        soup = BeautifulSoup(citations.text, 'html.parser')
        link_tags = soup.find_all('a', id=True)
        print(link_tags)
        for link in link_tags:
            file.write(f"{link['href']}")
        paper = paper.replace(f'start={index}', f'start={int(index)+10}')
        index = str(int(index) + 10)
    file.close()
    
def getAllCitationUrls(papers):
    for paper in papers:
        getCitationUrls(paper)




test_url = "https://scholar.google.com/scholar?start=00&oi=bibs&hl=en&cites=8876951269706202931"


getCitationUrls(test_url)

# journalList = extractListfromFile() 

