from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from googleUrlGetter import make_request
import os, time, random, csv
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
    sorted_unique = dict(sorted(uniqueUrls.items(), key=lambda item: item[1], reverse=True))
    return sorted_unique

def writeUniqueJournalUrlsToFile(sorted_unique, filepath="files/journalCounts.txt"):
    file = open(filepath, "w", encoding="utf-8")
    for key in sorted_unique.keys():
        file.write(f"{key} {sorted_unique[key]}\n")
    file.close()
    
    

         
def getJournalAuthors(journal):
    affMap = {}
    if journal.startswith("https://www.sciencedirect.com/science/article/"):
        def scienceDirectFetch():
            driver = webdriver.Chrome()
            driver.implicitly_wait(3)
            driver.get(journal)
            author = driver.find_element(By.CLASS_NAME, "button-link.button-link-secondary.button-link-underline")
            while author:
                author_info = []
                try:
                    author.click()
                    fname = author.find_element(By.CLASS_NAME, 'given-name').text
                    lname = author.find_element(By.CLASS_NAME, 'text.surname').text
                    affiliations = driver.find_elements(By.XPATH, '//*[@id="side-panel-author"]/div')
                    for aff in affiliations:
                        if(aff.text != ""):
                            author_info.append(aff.text) 
                    affMap[fname+" "+lname] = author_info[1]  
                    author = author.find_element(By.XPATH, "following::button[contains(@class, 'button-link') and contains(@class, 'button-link-secondary') and contains(@class, 'button-link-underline')][1]")
                except NoSuchElementException:
                    print('checked all authors')
                    break
                except ElementClickInterceptedException:
                    close_popup = driver.find_element(By.CLASS_NAME, '_pendo-close-guide')
                    close_popup.click()
                except StaleElementReferenceException:
                    author = driver.find_element(By.CLASS_NAME, "button-link.button-link-secondary.button-link-underline")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:    
                    driver.close()
        scienceDirectFetch()
    elif journal.startswith("https://link.springer.com/article/"):  
        def springerFetch(): 
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(3)
                driver.get(journal)
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
            finally:    
                    driver.close()
        springerFetch()  
    elif journal.startswith("https://www.mdpi.com/"):
        def mdpiFetch():
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(3)
                driver.get(journal)
                locations = {}
                authors_span = driver.find_elements(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[2]/span')
                affiliations = driver.find_elements(By.XPATH, '//*[@id="abstract"]/div[2]/article/div/div[5]/div/div')
                if len(affiliations) > 2:
                    for author_span in authors_span:
                        name = author_span.find_element(By.XPATH, './/*[@class="profile-card-drop"]')
                        number_elem = author_span.find_element(By.XPATH, './/sup')
                        number = number_elem.text.replace(',', '').replace('*', '').replace('†', '').replace('‡', '')
                        for num in number:
                            affMap[name.text] = int(num)
                    for aff in affiliations:
                        num_span = aff.find_element(By.XPATH, './div[@class="affiliation-item"]/sup')
                        if not num_span.text.isnumeric():
                            continue
                        num = int(num_span.text)
                        location = aff.find_element(By.XPATH, './div[2]').text
                        locations[num] = location
                    for author in affMap.keys():
                        location_num = affMap[author]
                        affMap[author] = locations[location_num]
                else:
                    location = affiliations[0].find_element(By.XPATH, './div[contains(@class, "affiliation-name")]').text
                    for author_span in authors_span:
                        name = author_span.find_element(By.XPATH, './/*[@class="profile-card-drop"]')
                        affMap[name.text] = location  
            finally:    
                driver.close()
        mdpiFetch()
    elif journal.startswith("https://ieeexplore.ieee.org/"):
        def ieeeFetch():
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(3)
                driver.get(journal)
                authors = driver.find_elements(By.XPATH, '//*[contains(@class, "authors-info-container") and contains(@class, "authors-minimized")]/span')
                for author in authors:
                    try:
                        name = author.find_element(By.XPATH, './span[1]/a/span').text   
                        tooltip = author.find_element(By.XPATH, './span')
                        hov = ActionChains(driver).move_to_element(tooltip)
                        hov.perform()
                        location = tooltip.find_element(By.XPATH, './ngb-tooltip-window/div[2]/span').text
                        affMap[name] = location
                    except NoSuchElementException:
                        continue
            finally:    
                driver.close()
        ieeeFetch()
    else:
        print(f"{journal} is not part of websites supported yet")
    return(affMap)

def getCountriesFromText(text):
    country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
    output = []
    for country in country_list:
        if country in text:
            output.append(country)
    return output

def getExistingCsvEntries(filepath="files/author_data.csv"):
    existing_entries = {}
    csv_file = open(filepath, "r", encoding='utf-8')
    lines = csv_file.readlines()
    csv_file.close()
    for line in lines:
        url = line.split(',')[0]
        existing_entries[url] = True
    return existing_entries

def getAuthorsAndWriteToCsv(existing_entries={}, dir='files/citations', csv_filepath="files/author_data.csv", csv_headers = ["Journal Url", "Corresponding Journal Id", "Authors", "Locations"]):
    dir_list = os.listdir(dir)
    for i, filename in enumerate(dir_list):
        print(f"looking through file {i}/{len(dir_list)}, {filename}")
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath):
            file = open(filepath, 'r', encoding='utf-8') 
            
            lines = file.readlines()
            file.close()
            for i, url in enumerate(lines):
                url = url.strip('\n')
                if url.startswith("ignore:") or url in existing_entries:
                    print(f"skipping {url}")
                    continue
                affiliations = None
                for attempt in range(5):
                    try:
                        affiliations = getJournalAuthors(url)
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed for {url}: {e}")
                else:
                    print(f"{url} failed after 5 attempts, skipped")
                    continue
                if not affiliations:
                    print(f"{url} implementation not finished, skipped")
                    continue
                print(f"searching {url} for authors")
                authorString = ""
                locationsString=""
                for author in affiliations.keys():
                    authorString+=f"&{author}"
                    locationsString+=f"&{affiliations[author]}"
                authorString = authorString[1:]
                locationsString = locationsString[1:]
                csv_row = {csv_headers[0]:url, csv_headers[1]:filename.replace('.txt', ''), csv_headers[2]:authorString, csv_headers[3]:locationsString }
                #what article cited this, which of dr. mahdi's articles was cited, authors & separated, locations & separated
                csv_file = open(csv_filepath, "a", newline='', encoding='utf-8')
                writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                writer.writerow(csv_row)
                lines[i] = "ignore:" + lines[i]
                file = open(filepath, 'w', encoding='utf-8') 
                file.writelines(lines)
                file.close()
                csv_file.close()
    
journal_url = "https://www.sciencedirect.com/science/article/pii/S0378778824009460" #current test


if __name__ == "__main__":

    # affMap = getJournalAuthors(journal_url)
    # for key in affMap.keys():
    #     print(f"Author: {key}")
    #     print(f"Affiliations: {affMap[key]}")
    
    
    # unique = getUniqueJournalUrls()
    # writeUniqueJournalUrlsToFile(unique)
    # input('continue?')
    
    
    existing_entries = getExistingCsvEntries()
    getAuthorsAndWriteToCsv(existing_entries)
    
                    
        