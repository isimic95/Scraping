from urllib.request import urlopen
import requests
from selenium import webdriver
import csv
from lxml import etree
import json
from collections import OrderedDict
import sys

paths = []
url = ""
linkElementa = ""
nextPutanja = ""
linkPrefix = ""

with open(sys.argv[1], 'r') as f:
    i = 0
    for line in f:
        if(i==0):
            url = line.rstrip()
            print(url)
            i+=1
            continue
        if(i==1):
            linkElementa = line.rstrip()
            i+=1
            continue
        if(i==2):
            nextPutanja = line.rstrip()
            i+=1
            continue
        if(i==3):
            linkPrefix = line.rstrip()
            i+=1
            continue

        splitLine = line.rstrip().split("\t")
        paths.append((splitLine[0],splitLine[1]))

html = urlopen(url).read().decode("utf-8");
driver = webdriver.PhantomJS(executable_path="phantomjs")
driver.get(url)

dom = etree.fromstring(html, parser=etree.HTMLParser(), base_url=url)

links = []
flag = True

i = 1
while(flag):
    print("Scrapeam " + str(i) + ". stranicu")
    for link in dom.xpath(linkElementa):
        print(link)
        if(link not in links):
            links.append(linkPrefix + link)
    try:
        driver.find_element_by_xpath(nextPutanja).click()
        dom = etree.fromstring(driver.page_source, parser=etree.HTMLParser(), base_url=url)
        i += 1
    except Exception as e:
        i+=1
        flag = False

for link in links:
    print(link)
    i = len(paths)
    row = OrderedDict()
    row['link'] = link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    res = requests.get(link, headers=headers)
    try:
        dom = etree.fromstring(res.text, parser=etree.HTMLParser(), base_url=url)
    except e:
        print("Error while scraping!")
    for path in paths:
        items = []
        for item in dom.xpath(path[0]):
            items.append(item.strip())
        row[path[1]] = items

    with open('knjige.csv', 'a', encoding="utf-8") as f:
        writer = csv.DictWriter(
                f,
                list(row.keys()),
                dialect='excel',
            )
        writer.writerow(row)

    with open('knjige.txt', 'a', encoding="utf-8") as f:
        json.dump(row, f)