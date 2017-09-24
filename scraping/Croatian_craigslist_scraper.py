from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import wait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
import csv
import re
import datetime
import sys, getopt

opt, arg = getopt.getopt(sys.argv[1:], 'wts')

url = "http://www.njuskalo.hr/prodaja-stanova/" + arg[1]
base_url = "http://www.njuskalo.hr"

driver = webdriver.PhantomJS(executable_path="phantomjs")
driver.get(url)

data = []
godina=2017
previous_page = "filled after first page switch"

def page_has_loaded(self):

    page_state = self.execute_script('return document.readyState;')
    return page_state == 'complete'

while godina > 2015 :

    bsObj = BeautifulSoup(driver.page_source, "html.parser")

    for item in bsObj.findAll("article", {"class":"entity-body cf"}):
        if "/nekretnine/" in item.h3.a.attrs["href"]:
            try:
                link = base_url + item.h3.a.attrs["href"]
                kvadratura = item.find("div", {"class":"entity-description-main"}).br.get_text()
                cijena = item.find("strong", {"class":"price price--hrk"}).get_text()
                kvadratura = kvadratura[re.search('\d', kvadratura).start()::]

                datum = item.find("time", {"class":"date--full"}).get_text()
                godina = int(datum.split(".")[2])
                print(link)

                stan = {
                    'link': link,
                    'kvadratura': kvadratura,
                    'cijena': cijena,
                    'datum': datum
                }
                data.append(stan)

            except:
                pass

    next_page = driver.find_element_by_xpath('//ul[@class="Pagination-items cf"]/li[last()]/a').get_attribute("href")
    if next_page == previous_page:
        break
    else:    
        driver.get(next_page)
        previous_page=next_page
    
    try:
        wait.WebDriverWait(driver, 10).until(page_has_loaded)
    except TimeoutException:
        break

with open('stanovi' +arg[1]+'.csv', 'w') as f:
                writer = csv.DictWriter(
                    f,
                    ['link', 'kvadratura', 'cijena', 'datum'],
                    dialect='excel',
                )
                for row in data:
                    writer.writerow(row)




