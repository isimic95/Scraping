from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

#time.sleep(2400)
html = urlopen("http://www.sportstats.com/soccer/")
bsObj = BeautifulSoup(html, "html.parser")
driver = webdriver.PhantomJS(executable_path="phantomjs")

row = {}
links = []

list_of_td = bsObj.findAll("td", {"class": "result-stats"})
for td in list_of_td:
    links.append("http://www.sportstats.com/" + td.a.attrs["href"])

visited_links = []
try:
    with open('danas[nogomet_links].txt', 'r') as f:
        for line in f:
            visited_links.append(line[:-2] + "/")
except:
    pass

print(visited_links)
for link in links:
    if link in visited_links:
        continue

    print(link)

    try:
        driver.get(link)
        print('got it')
    except Exception as e:
        print("greska1")
        print(e)
        continue
    match_name = link.split("/")[7].split("-")[:-1]
    match_name = " ".join(match_name)
    print(match_name)
    time.sleep(1.5)

    element_1 = None
    sub_element_1 = None

    try:
        element_1 = driver.find_element_by_xpath(
            "//ul[@id='tabSwitch_teamfilterresultspos_72']/li[1]")
        sub_element_1 = driver.find_element_by_xpath(
            "//ul[@id='tabSwitch_teamfilterresultspos_72']/li[1]/a[1]")
    except:
        pass

    #element_2 = driver.find_element_by_xpath(
    #    "//ul[@id='tabSwitch_homeawayfilterresultspos_72']/li[1]")
    try:
        driver.find_element_by_xpath(
            "//ul[@id='tabSwitch_homeawayfilterresultspos_72']/li[1]/a[1]").click()
    except:
        pass
        
    time.sleep(0.5)

    element_3 = None
    sub_element_3 = None

    try:
        element_3 = driver.find_element_by_xpath(
            "//ul[@id='tabSwitch_teamfilterresultspos_73']/li[1]")
        sub_element_3 = driver.find_element_by_xpath(
            "//ul[@id='tabSwitch_teamfilterresultspos_73']/li[1]/a[1]")
    except:
        pass

    #element_4 = driver.find_element_by_xpath(
    #    "//ul[@id='tabSwitch_homeawayfilterresultspos_73']/li[1]")
    driver.find_element_by_xpath(
        "//ul[@id='tabSwitch_homeawayfilterresultspos_73']/li[1]/a[1]").click()
    time.sleep(1)

    if element_1 != None:
        ActionChains(driver).move_to_element(element_1).click(sub_element_1).perform()
    time.sleep(1)

    #ActionChains(driver).move_to_element(element_2).click(sub_element_2).perform()
    #time.sleep(1)

    if element_3 != None:
        ActionChains(driver).move_to_element(element_3).click(sub_element_3).perform()
    time.sleep(1)

    #ActionChains(driver).move_to_element(element_4).click(sub_element_4).perform()
    #time.sleep(1)

    for i in range(10):
        try:
            driver.find_element_by_xpath("//div[@class='tableFooterTeaser more']/a[1]").click()
            print("1. Click")
            time.sleep(1)
        except Exception as e:
            break
    for i in range(10):
        try:
            driver.find_element_by_xpath("//div[@class='tableFooterTeaser more']/a[1]").click()
            print("2. Click")
            time.sleep(1)
        except Exception as e:
            break
    for i in range(10):
        try:
            driver.find_element_by_xpath("//div[@class='tableFooterTeaser more']/a[1]").click()
            print("3. Click")
            time.sleep(1)
        except Exception as e:
            break

    team1_scores = []
    team2_scores = []
    mutual_scores = []

    team1_elem = driver.find_elements_by_xpath(
        "//table[contains(@id, 'resultspos_72')]/tbody/tr/td[@class='result-neutral']/a")
    team2_elem = driver.find_elements_by_xpath(
        "//table[contains(@id, 'resultspos_73')]/tbody/tr/td[@class='result-neutral']/a")
    mutual_elem = driver.find_elements_by_xpath(
        "//table[contains(@id, 'maintable_')]/tbody/tr/td[@class='result-neutral']/a")

    for element in team1_elem:
        team1_scores.append(element.text)
    print('Pass 1')
    for element in team2_elem:
        team2_scores.append(element.text)
    print('Pass 2')
    for element in mutual_elem:
        mutual_scores.append(element.text)
    print('Pass 3')
    row =   {
                'match_name' : match_name,
                'team1_scores' : team1_scores,
                'team2_scores' : team2_scores, 
                'mutual_scores' : mutual_scores
            }
    print("gotovo")
    with open('danas[nogomet].csv', 'a') as f:
        writer = csv.DictWriter(
                        f,
                        ['match_name', 'team1_scores', 'team2_scores', 'mutual_scores'],
                        dialect='excel',
                     )
        writer.writerow(row)

    with open('danas[nogomet_links].txt', 'a') as f:
        f.write(link+"\n")