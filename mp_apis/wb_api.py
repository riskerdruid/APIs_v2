import requests
import json
from dataclasses import dataclass

url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
headers = {
    "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwNDE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MTM1MzEzMiwiaWQiOiIwMTk2NmNmYi01NDMzLTczY2MtYTVjMi03ZDQxMzRmMzhmYzYiLCJpaWQiOjU2Njg3MTAxLCJvaWQiOjM0MzM0LCJzIjo3OTM0LCJzaWQiOiJjNjM5OTY0OS0xYWZhLTU5MmEtYTI2My02NmIyOWRiYzJlMjkiLCJ0IjpmYWxzZSwidWlkIjo1NjY4NzEwMX0.xIYS1VwmLG2Fw_x0y12bhtdlL9TanXWFEW0mA6UUdOS5gULVm2nuwGaqLtJCkM6blWyKR61AZ8EYE2AsIIfe3A"
}
data = {
    "limit": 999,
    "offset": 0
}

@dataclass
class WbPrice:
    vendorCode: str
    nmID: str
    price: int
    discounter_price: float
    discount: int
    card_price: float

def get_wb_final_price(nm_id: int, app_type: str = '1', dest: str = '-1257786') -> float:
    url = 'https://card.wb.ru/cards/detail'
    params = {
        'nm': str(nm_id),
        'appType': app_type,
        'curr': 'rub',
        'dest': dest,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    prods = resp.json()['data']['products']
    if len(prods) > 0:
        prod = prods[0]
        price_u = prod.get('salePriceU') or prod.get('priceU')
        if price_u:
            return price_u / 100
    return 0

def get_wb_items()->list[WbPrice]|None:
    prices = []
    while True:
        response = requests.get(url, params=data, headers=headers)
        if response.status_code != 200:
            print(response.text)
            return
        result = json.loads(response.text)
        items = result['data']['listGoods']
        if len(items) == 0:
            break
        for j in range(len(items)):
            item = items[j]
            for size in item['sizes']:
                price = WbPrice(item['vendorCode'], item['nmID'],
                                size['price'], size['discountedPrice'],
                                item['discount'], get_wb_final_price(item['nmID']))
                prices.append(price)
        data['offset'] += data['limit']
        print('Получено 999 товаров с wb')
    return prices