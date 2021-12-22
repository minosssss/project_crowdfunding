import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import *
import time
import os
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')  # 내부 창을 띄울 수 없으므로 설정
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument('disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=chrome_options)
time.sleep(1)

def get_last():
    pages = driver.find_elements_by_class_name("page-link")
    last = int(pages[-2].text)
    return last


def get_urls(last):
    links = []
    for page in range(1, last+1):
        urls = driver.get(
            f"https://programmers.co.kr/job?min_salary=&min_career=&min_employees=&order=recent&page={page}")
        time.sleep(1)
        print(f"{page} 스크랩 중")
    #         html = driver.page_source
    #         soup = bs4.BeautifulSoup(html,"html.parser")
    #         hrefs = soup.select(.position-title).get['href']
        js = 'return [...document.querySelectorAll(".position-title a")].map(a=>a.href)'
        hrefs = driver.execute_script(js)

        for href in hrefs:
            link = href
            links.append(link)
    return links


def get_info(links):
    recruit = []
    for number, link in enumerate(links):
        informations = {}
        stackinfo = []
        url = link
        driver.get(url)
        time.sleep(1)
        company = driver.find_elements_by_xpath("//h4[@class='sub-title'][1]")
        notice = driver.find_elements_by_xpath("//h2[@class='title']")

        stacks = driver.find_elements_by_xpath(
            "//tr[@class='heavy-use']//td//code")
        index = driver.find_elements_by_xpath(
            "//tbody//tr//td[@class='t-label']")
        content = driver.find_elements_by_xpath("//td[@class='t-content']")
        for c, n in zip(company, notice):

            company = c.text
            notice = n.text
        for s in stacks:
            stack = s.text
            stackinfo.append(stack)
        for i, c in zip(index, content):
            info = i.text
            content = c.text
            informations[info] = content
        doc = {
            'notice': notice,
            'url': url,
            'stack': stackinfo,
            'company': company,
            'information': informations
        }
        index = number+1
        recruit.append(doc)
        print(f"{index}번째 저장중")
        start = time.time()
        producer.send('test', value=doc)
        producer.flush()

    print("소요시간 :", time.time() - start)
    db.coffee.insert_one(doc)
    print('완료!', title)

# 기존 coffee 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.


def insert_all():
    db.recruit.drop()  # coffee 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_coffee(url)


# ### 실행하기
insert_all()