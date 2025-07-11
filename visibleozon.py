import requests
from typing import List, Dict

CLIENT_ID = "9305"
API_KEY = "a43365ad-684f-48f5-b21d-16c8699714d3"
HEADERS = {
    "Client-Id": CLIENT_ID,
    "Api-Key": API_KEY,
    "Content-Type": "application/json"
}
API_URL = "https://api-seller.ozon.ru/v3/product/list"

def get_visible_ozon_ids(offer_ids: List[str]) -> Dict[str, bool]:
    
    visible_map = {}
    batch_size = 100
    for i in range(0, len(offer_ids), batch_size):
        batch = offer_ids[i:i + batch_size]
        payload = {
            "filter": {"offer_id": batch},
            "limit": batch_size,
            "with_excluded": False,
            "with_archived": False
        }
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            if "result" in data and "items" in data["result"]:
                for item in data["result"]["items"]:
                    offer_id = item.get("offer_id")
                    has_stock = item.get("has_fbo_stocks", False) or item.get("has_fbs_stocks", False)
                    archived = item.get("archived", False)
                    visible_map[offer_id] = has_stock and not archived
        except requests.exceptions.RequestException as e:
            print(f" Ошибка запроса: {str(e)}")
    return visible_map