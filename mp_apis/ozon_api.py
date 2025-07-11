import requests
import json
import base64
from dataclasses import dataclass

url = "https://api-seller.ozon.ru/v5/product/info/prices"
headers = {
    "Client-Id": "9305",
    "Api-Key": "a43365ad-684f-48f5-b21d-16c8699714d3"
}

@dataclass
class OzonPrice:
    offer_id: str
    old_price: float
    min_price: float
    marketing_price: float
    external_index_data: float

def get_data(cursor: list):
    data = {
        "cursor": base64.b64encode(str(cursor).replace(' ', '').encode()).decode(),
        "filter": {
        },
        "limit": 999,
    }
    return data

items: list[OzonPrice] = []
cursor = []


def get_ozon_items() -> list[OzonPrice]:
    response = requests.post(url, json=get_data(cursor), headers=headers)
    result = json.loads(response.text)
    for j in range(len(result['items'])):
        item = result['items'][j]

        price = OzonPrice(item['offer_id'], item['price']['old_price'], item['price']['min_price'],
                        item['price']['marketing_price'], item['price_indexes']['external_index_data']['min_price'])
        cursor.append(result['items'][j]['product_id'])
        items.append(price)

    total = result['total']
    k = 500
    while k < total:
        response = requests.post(url, json=get_data(cursor[-2:]), headers=headers)
        result = json.loads(response.text)
        for j in range(1, len(result['items'])):
            item = result['items'][j]
            price = OzonPrice(item['offer_id'], item['price']['old_price'], item['price']['min_price'],
                        item['price']['marketing_price'], item['price_indexes']['external_index_data']['min_price'])
            cursor.append(result['items'][j]['product_id'])
            items.append(price)
        print('Получено 500 товаров ozon')
        k += 499
    
    return items