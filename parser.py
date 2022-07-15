import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.kivano.kg/mobilnye-telefony"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    "accept": "*/*",
}
LINK = "https://www.kivano.kg"
FILE = "phones.csv"


def get_html(headers, url, params=None):
    response = requests.get(url, params=params, headers=headers)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="item product_listbox oh")
    phones = []
    for i in items:
        phones.append({
            "title": i.find("strong").get_text(),
            "image": LINK + i.find("img").get("src"),
            "description": i.find("div", class_="product_text pull-left").get_text().replace("\n\n", ""),
            "price": i.find("div", class_="listbox_price text-center").get_text().replace("\n", ""),

        })
    return phones

def save_file(content, file):
    with open(file, "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Название продукта", "Картинка",
                         "Описание", "Цена",])
        for i in content:
            writer.writerow([
                i['title'], i['image'],
                i['description'], i['price']
                             ])


def get_parse_result():
    html = get_html(HEADERS, URL)
    content = get_content(html.text)
    save_file(content, FILE)


get_parse_result()




