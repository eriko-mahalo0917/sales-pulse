# =========================================
# import
# ※sys.pathの追加を先に行う必要がある
# 　理由：
# 　utilsフォルダをimport対象に追加してから
# 　from utils ... を読み込まないと ModuleNotFoundError になるため
# =========================================
import os
import sys
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.logger import SimpleLogger
from utils.helper_path import data_path


#=========================================

class LoaderFlow:
    def __init__(self):
        self.logger_setup = SimpleLogger()
        self.logger = self.logger_setup.get_logger()
    # -----------------
    # 1つ目のフロー：ファイルパス取得
    # ・utils/helper_path.pyを使用してdata/sales.csvのパスを取得する
    # ・EXE化しても動くように相対パスベースで管理する
    # -----------------
    def get_file_path(self):
        self.logger.info("CSVファイルのパスを取得します")
        csv_file_path = data_path("sales.csv")
        self.logger.info(f"取得したCSVパス: {csv_file_path}")
        return csv_file_path

    # -----------------
    # 2つ目のフロー：CSVファイル存在チェック
    # ・取得したパスにファイルが存在するか確認する
    # ・存在しない場合はエラーとして処理を中断する
    # -----------------
    def check_file_exists(self,csv_file_path) -> None:
        self.logger.info(f"ファイル存在確認: {csv_file_path}")
        #Pathのメソッド.exists()
        #　・指定したパスにファイルが存在するかをチェックする
        if not csv_file_path.exists():
            self.logger.error(f"CSVファイルが見つかりません:{csv_file_path}")
            #ファイルがないなら止める（安全設計）
            raise FileNotFoundError(f"CSVファイルが見つかりません:{csv_file_path}")
        self.logger.info("CSVファイルの存在確認OK")
        

    # -----------------
    # 3つ目のフロー：CSVファイル読み込み準備
    # ・utf-8形式でファイルを開く
    # ・csv.DictReaderを使用して読み込み準備を行う
    # ・すべてのデータをリストとして取得する
    # -----------------
    def load_csv(self, csv_file_path) -> list[dict[str, str]]:
        self.logger.info("CSVファイルを読み込み開始します")
        
        #ファイルを開く(読み取りモード:UTF=8)
        #with構文 →　自動でファイルを閉じる安全な書き方
        #r → 読み取りモード
        with open(csv_file_path, mode= "r", encoding="utf-8") as csv_file:
            
            # CSVを辞書形式で読み込む
            # 例：{"date": "2026-05-01", "item": "apple", "sales": "500"}
            reader = csv.DictReader(csv_file)
            
            #全行をリストとして取得する
            #リスト内方表記
            #[ 出したいもの  for 1件ずつ取得  if 条件 ]
            sales_records =  [one_row_data for one_row_data in reader]
            
            self.logger.info(f"CSV読み込み完了:{len(sales_records)}件取得しました")
            return sales_records
            
    # -----------------
    # 4つ目のフロー：データ読み込み処理
    # ・3つ目のフローで読み込んだ sales_records を受け取る
    # ・CSVは文字列（str）として読み込まれるため、必要な型へ変換する
    # ・sales（売上）は str → int に変換する
    # ・CSVの再読込みは行わず、メモリ上のデータを加工する
    # ・読み込み処理と整形処理を分けることで、役割を明確にする
    # -----------------
    def format_sales_data(self, sales_records: list[dict[str, str]]) -> list[dict[str, str|int]]:
        self.logger.info("CSVデータの型変換を開始します")
        #空のリストを作る
        formatted_sales_records : list[dict[str, str | int]] = []
        
        #1件ずつデータを取得する
        for sales_record in sales_records:
            #整形後の１件文データを作成する
            formatted_record = {
                "date": sales_record["date"],
                "item": sales_record["item"],
                "sales": int(sales_record["sales"])
            }
            
            #整形したデータを作成した空データへ追加する
            formatted_sales_records.append(formatted_record)
        
        self.logger.info(f"型変換完了:{len(formatted_sales_records)}件整形しました")
        return formatted_sales_records
    
    
1
if __name__ == "__main__":
    #クラスを生成
    loader_flow = LoaderFlow()
    
    #①CSVパス取得
    csv_file_path = loader_flow.get_file_path()
    
    #②ファイルの存在チェック
    loader_flow.check_file_exists(csv_file_path)
    
    #③CSV読み込み
    sales_records = loader_flow.load_csv(csv_file_path)
    
    #④データ整形
    formatted_sales_records = loader_flow.format_sales_data(sales_records)
    
    #確認
    print("==============整形後のデータ===============")
    for record in formatted_sales_records:
        print(record)