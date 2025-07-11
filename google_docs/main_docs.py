import gspread
from google.oauth2.service_account import Credentials
import pathlib

scoped = ["https://www.googleapis.com/auth/spreadsheets"]
creds_path = pathlib.Path(__file__).parent.joinpath('credentials.json')
creds = Credentials.from_service_account_file(creds_path, scopes=scoped)
client = gspread.authorize(creds)

sheet_id = "1APhXex5bbDdMzRL7gZGbrBCazL3nJLfvcybMzGHa76s"
sheet = client.open_by_key(sheet_id).sheet1

def update_docs(col_letter: str, prices: list):
    sheet.batch_update(
        [{
            'range': f'{col_letter}3:{col_letter}{len(prices)+3}',
            'values': list(map(lambda x: [x], prices))
        }]
    )

# [0,0,0,0]
# [[0], [0], [0], [0]]

# def start_updates():
#     schedule.every(__UPDATE_INTERVAL).seconds.do(__update_docs)
#     __update_docs()

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
