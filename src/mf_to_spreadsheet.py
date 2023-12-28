import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_gspread(jsonf,key):
    # 認証情報の設定
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)

    # SpreadSheetへの接続
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(key).sheet1
    return worksheet
  
def main():
  jsonf = '/root/credentials/mf-to-spreadsheet-9de8d743214d.json'
  spread_sheet_key = '1zo_dhWooKj3JWaKn9_zaihJXCdysZl6TESzst3WsuKI'

  worksheet = connect_gspread(jsonf, spread_sheet_key)
  data = worksheet.get_all_values()
  print(data[3])

if __name__ == '__main__':
  main()
