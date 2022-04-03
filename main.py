from bs4 import BeautifulSoup as bs
import requests
import csv

URL = "https://www.perekrestok.ru/cat/c/5/viski-burbon"
HEAD = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "accept": "*/*",
}

FILE = "output.csv"


def get_html(url, params=None):
    r = requests.get(url, params=params, headers=HEAD)
    return r.text


def get_content(html):
    soup = bs(html, "lxml")
    single_cards = soup.find_all("div", class_="sc-hYAvag kdpgXU")
    price_list = []
    for i in single_cards:
        name = (
            i.find("div", class_="product-card__content")
            .find("div", class_="product-card-title__wrapper")
            .find("div", class_="product-card__title")
        ).text
        new_price = (
            i.find("div", class_="product-card__content")
            .find("div", class_="product-card__control")
            .find("div", class_="product-card__price")
            .find("div", class_="price-new")
            .text
        )
        old_price = (
            i.find("div", class_="product-card__content")
            .find("div", class_="product-card__control")
            .find("div", class_="product-card__price")
            .find("div", class_="price-old")
        )
        if old_price is None:
            price_list.append(
                {
                    "sku": name.replace("\u20bd", "").replace("\xea", "").replace("\xe8", "").replace("\xfc", ""),
                    "new_price": new_price.replace("\u20bd", "")
                    .replace("\xea", "")
                    .replace("\xe8", "")
                    .replace("\xfc", ""),
                    "old_price": None,
                }
            )
        else:
            price_list.append(
                {
                    "sku": name.replace("\u20bd", "").replace("\xea", "").replace("\xe8", "").replace("\xfc", ""),
                    "new_price": new_price.replace("\u20bd", "")
                    .replace("\xea", "")
                    .replace("\xe8", "")
                    .replace("\xfc", ""),
                    "old_price": old_price.text.replace("\u20bd", "")
                    .replace("\xea", "")
                    .replace("\xe8", "")
                    .replace("\xfc", ""),
                }
            )
    return price_list


def save_file(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [
                "SKU",
                "Отпускная цена",
                "Старая цена",
            ]
        )
        for item in items:
            writer.writerow(
                [
                    item["sku"],
                    item["new_price"],
                    item["old_price"],
                ]
            )


def parse():

    price_list = []
    html = get_html(URL)
    price_list.extend(get_content(html))
    save_file(price_list, FILE)
    print("Выполнено")


parse()


