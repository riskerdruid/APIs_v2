from mp_apis.ozon_api import get_ozon_items, OzonPrice
from mp_apis.wb_api import get_wb_items, WbPrice
from visibleozon import get_visible_ozon_ids 
from google_docs.main_docs import update_docs
import schedule
import time

def update_google_docs():
    print('Получение цен Ozon')
    ozon_prices = get_ozon_items()
    
    
    print('Проверка видимости товаров Ozon')
    visible_offers = get_visible_ozon_ids([p.offer_id for p in ozon_prices])
    
    
    for price in ozon_prices:
        if not visible_offers.get(price.offer_id, False):
            price.old_price = 0
            price.min_price = 0
            price.marketing_price = 0
            price.external_index_data = 0
    
    print('Получение цен WB')
    wb_prices = get_wb_items()
    
    print('Обновление Ozon в Google Таблице...')
    update_docs('B', list(map(lambda p: p.offer_id, ozon_prices)))
    update_docs('C', list(map(lambda p: p.old_price, ozon_prices)))
    update_docs('D', list(map(lambda p: p.min_price, ozon_prices)))
    update_docs('E', list(map(lambda p: p.marketing_price, ozon_prices)))
    update_docs('F', list(map(lambda p: p.external_index_data, ozon_prices)))
    
    print('Обновление WB в Google Таблице...')
    update_docs('H', list(map(lambda p: p.vendorCode, wb_prices)))
    update_docs('M', list(map(lambda p: p.nmID, wb_prices)))
    update_docs('I', list(map(lambda p: p.price, wb_prices)))
    update_docs('J', list(map(lambda p: p.discounter_price, wb_prices)))
    update_docs('K', list(map(lambda p: p.discount, wb_prices)))
    update_docs('L', list(map(lambda p: p.card_price, wb_prices)))
    
    print('Обновление завершено\n')

def start_updates():
    schedule.every(6).hours.do(update_google_docs)
    update_google_docs()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__': start_updates()