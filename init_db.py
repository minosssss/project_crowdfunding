import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


# DB에 저장할 제품 상세페이지 url을 가져오기
def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    link = requests.get(
        f"https://zerocoffee.net/product/list.html?cate_no=304&page=1", headers=headers)

    soup = BeautifulSoup(link.text, 'html.parser')
    products = soup.select('button > img')  # 상품상세 soup
    page_no = []
    for i in products:
        page_no_list = i.get('product_no')
        page_no.append(int(page_no_list))
    urls = []
    for j in page_no:
        url = f"https://zerocoffee.net/product/detail.html?product_no={j}&cate_no=304&display_group=1"
        urls.append(url)
    return urls

# 출처 url로부터 상품들의 사진, 이름, 가격, 상세사진을 가져오고 coffee 콜렉션에 저장.
def insert_coffee(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    link = requests.get(url, headers=headers)

    soup2 = BeautifulSoup(link.text, 'html.parser')
    info_sub = 'https://zerocoffee.net/'
    main_img = soup2.select_one('div.thumbnail img').get('src')
    titles = soup2.select_one('div.thumbnail img').get('alt').replace('제로커피 ', '').strip()
    price = soup2.select_one('#span_product_price_text').get_text()
    info = soup2.select_one('#prdDetail img').get('ec-data-src')
    product_no = soup2.select_one(' div.guideArea > span > a').get('product_no')
    info_img = info_sub + info
    if titles[0] == '2':
        title = titles[5:] + " " + titles[0:4]
    else:
        title = titles
    doc = {
        'main_img': main_img,
        'title': title,
        'price': price ,
        'info_img': info_img,
        'product_no':product_no,
    }

    db.coffee.insert_one(doc)
    print('완료!', title)

# 기존 coffee 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.coffee.drop()  # coffee 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_coffee(url)

# ### 실행하기
insert_all()
