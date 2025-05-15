from selenium import webdriver
from selenium.webdriver.common.by import By
from googleCrawler import make_request

journal_url = "https://link.springer.com/article/10.1007/s10973-022-11896-2"




def getJournalAuthors(journal):
    affMap = {}
    path = "../chromedriver-win64"
   
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
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
    else:
        return {}
    
    return(affMap)

def getCountriesFromText(text):
    country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
    output = []
    for country in country_list:
        if country in text:
            output.append(country)
    return output

affMap = getJournalAuthors(journal_url)
for key in affMap.keys():
    print(f"Author: {key}")
    print(f"Affiliations: {affMap[key]}")
   