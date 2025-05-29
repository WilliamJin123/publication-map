from selenium import webdriver
from selenium.webdriver.common.by import By
from googleCrawler import make_request
import os, time, random
from urllib.parse import urlparse


def getUniqueJournalUrls(dir="./files/citations"):
    uniqueUrls = {}
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if os.path.isfile(file_path):
            file = open(file_path, 'r', encoding='utf-8')
            lines = file.readlines()
            for line in lines:
                parsed = urlparse(line)
                base_url = f"{parsed.scheme}://{parsed.netloc}/"
                if not uniqueUrls.get(base_url):
                    uniqueUrls[base_url] = 1 
                else:
                    uniqueUrls[base_url] += 1
            file.close()
    return uniqueUrls

         
def getJournalAuthors(journal):
    affMap = {}
    
   
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    # time.sleep(random.randint(3,5))
    driver.get(journal) 
    if journal.startswith("https://www.sciencedirect.com/science/article/"):
        def scienceDirectFetch():
            authors = driver.find_elements(By.CLASS_NAME, "button-link.button-link-secondary.button-link-underline")
            for author in authors:
                author_info = []
                author.click()
                fname = author.find_element(By.CLASS_NAME, 'given-name').text
                lname = author.find_element(By.CLASS_NAME, 'text.surname').text
                affiliations = driver.find_elements(By.XPATH, '//*[@id="side-panel-author"]/div')
                for aff in affiliations:
                    if(aff.text != ""):
                        author_info.append(aff.text) 
                affMap[fname+" "+lname] = author_info[1:]  
        scienceDirectFetch()
    elif journal.startswith("https://link.springer.com/article/"):
        def springerFetch(): 
            driver.find_element(By.XPATH, '/html/body/dialog/div/div/div[3]/button').click()
            authors = driver.find_elements(By.XPATH, '//*[@class="c-article-header"]/header/ul/li/a')
            for author in authors: 
                author_info = []
                author.click()
                author_info.append(author.text)
                affs = driver.find_elements(By.XPATH, '//*[@class="app-researcher-popup__author-list"]/li')
                for aff in affs:
                    if(aff.text != ""):
                        author_info.append(aff.text)
                affMap[author_info[0]] = author_info[1:]    
        springerFetch()  
    elif journal.startswith("https://www.mdpi.com/"):
        def mdpiFetch():
            locations = {}
            authors_span = driver.find_elements(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[2]/span')
            for author_span in authors_span:
                name = author_span.find_element(By.XPATH, './/*[@class="profile-card-drop"]')
                number = author_span.find_element(By.XPATH, './/sup')
                affMap[name.text] = int(number.text.replace(',', '').replace('*', '')) 
            affiliations = driver.find_elements(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[5]/div/div')
            for aff in affiliations:
                print(f"onto the next item!")
                num_span = aff.find_element(By.XPATH, './div[@class="affiliation-item"]/sup')
                if not num_span.text.isnumeric():
                    continue
                num = int(num_span.text)
                location = aff.find_element(By.XPATH, './div[2]').text
                print("location" + location)
                locations[num] = location
                
            for author in affMap.keys():
                location_num = affMap[author]
                affMap[author] = locations[location_num]
        mdpiFetch()
    elif journal.startswith("https://ieeexplore.ieee.org/"):
        def ieeeFetch():
            return
        ieeeFetch()
    else:
        print(f"{journal} is not part of websites supported yet")
        return {}
    return(affMap)

def getCountriesFromText(text):
    country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
    output = []
    for country in country_list:
        if country in text:
            output.append(country)
    return output


journal_url = "https://ieeexplore.ieee.org/abstract/document/7457675" #current test


if __name__ == "__main__":

    affMap = getJournalAuthors(journal_url)
    for key in affMap.keys():
        print(f"Author: {key}")
        print(f"Affiliations: {affMap[key]}")
    
    # unique = getUniqueJournalUrls()
    # sorted_unique = dict(sorted(unique.items(), key=lambda item: item[1], reverse=True))
    # file = open("files/journalCounts.txt", "w", encoding="utf-8")
    # for key in sorted_unique.keys():
    #     file.write(f"{key} {sorted_unique[key]}\n")
    # file.close()
    
    
    # https://www.sciencedirect.com/ 1311 done
    # https://ieeexplore.ieee.org/ 291
    # https://www.mdpi.com/ 205 done
    # https://link.springer.com/ 146 done
    # https://search.proquest.com/ 134
    # https://asmedigitalcollection.asme.org/ 115
    # https://www.sae.org/ 111
    # https://journals.sagepub.com/ 95
    # https://www.researchgate.net/ 71
    # https://www.tandfonline.com/ 42
    