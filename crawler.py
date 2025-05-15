# crawl google citations, look into journal articles, look into authors, fetch countries, store in csv file
import requests
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.90 Mobile/15E148 Safari/604.1"
    },
    {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    },
]

def make_request(url):
    headers = random.choice(alternate_headers)
    response = requests.get(url, headers=headers)
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
        print(f"Error: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='gs_ab_mdw')
    results = results[1].get_text()
    print(results)
    results = re.search(r"about\s+(\d[\d,\.]*)\s+result", results, re.IGNORECASE).group(1)
    results_length = int(results)
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