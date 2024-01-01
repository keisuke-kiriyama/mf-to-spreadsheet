from datetime import datetime
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

mf_to_ss_category = {
   '食費':'食費',
   '日用品':'日用品費',
   '趣味・娯楽':'趣味・娯楽',
   '交際費':'趣味・娯楽',
   '交通費':'趣味・娯楽',
   '衣服・美容':'特別費',
   '健康・医療':'健康・医療',
   '自動車':'趣味・娯楽',
   '教養・教育':'特別費',
   '特別な支出':'特別費',
   '現金・カード':'特別費',
   '水道・光熱費':'水道光熱費',
   '通信費':'通信費',
   '住宅':'住宅費',
   '税・社会保障':'特別費',
   '保険':'保険代',
   'その他':'特別費',
}

def load_expense_data():
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, 'src.csv')
   with open(file_path, newline='', encoding='cp932') as csvfile:
    reader = csv.reader(csvfile)
    expense_items = []
    for index, row in enumerate(reader):
        should_calculate = row[0] == '1'
        category = row[5]
        if index == 0 or not should_calculate or category == '収入':
            continue
        elif category == '未分類':
            print('未分類の項目があります。支出用途を設定してください。')
            sys.exit(1)
        elif category == '現金・カード':
            print('現金・カードの項目があります。支出用途を設定してください。')
            sys.exit(1)
        expense_items.append(
            {'date': row[1],
             'category': mf_to_ss_category[row[5]], 
             'price': int(row[3])})
    return expense_items

def get_month(expense_data):
    # 支出データは1ヶ月ごとのデータのため2項目目から該当月を取得する。(1項目目はカラム名)
    date_str = expense_data[0]['date']
    date = datetime.strptime(date_str, "%Y/%m/%d")
    return date.strftime("%Y/%m")

def aggregate_expense_data(expense_data):
    aggregated_data = {value: 0 for value in mf_to_ss_category.values()}
    for expense_item in expense_data:
        aggregated_data[expense_item['category']] += expense_item['price']
    return aggregated_data

def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(key).worksheet('メイン口座収支管理')
    return worksheet

def insert_aggregated_data_to_spreadsheet(aggregated_data, month, sheet):
    first_row_values = sheet.row_values(1)
    target_column = next((i for i, s in enumerate(first_row_values) if s == month), -1) + 1
    for category, price in aggregated_data.items():
        second_column_values = sheet.col_values(ord('B') - 64)
        target_row = next((i for i, s in enumerate(second_column_values) if s == category), '') + 1
        sheet.update_cell(target_row, target_column, price*-1)
  
def main():
    # 集計データの生成
    expense_data = load_expense_data()
    month = get_month(expense_data)
    aggregated_data = aggregate_expense_data(expense_data)

    # スプレッドシートと接続
    jsonf = '/root/credentials/mf-to-spreadsheet-9de8d743214d.json'
    spread_sheet_key = '1zo_dhWooKj3JWaKn9_zaihJXCdysZl6TESzst3WsuKI'
    sheet = connect_gspread(jsonf, spread_sheet_key)

    # スレッドシートにデータを挿入
    insert_aggregated_data_to_spreadsheet(aggregated_data, month, sheet)

if __name__ == '__main__':
    main()
