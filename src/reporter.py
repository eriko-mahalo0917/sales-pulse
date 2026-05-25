import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.logger import SimpleLogger
from utils.helper_path import output_path
from utils.config import REPORT_LABELS, CSV_HEADERS

import csv


class ReportFlow:
    def __init__(self):
        self.logger_setup = SimpleLogger()
        self.logger = self.logger_setup.get_logger()
        
        
    # -----------------
    # 1つ目のフロー：総売上CSV出力
    # ・AnalyzerFlowで計算した総売上を受け取る
    # ・総売上データをCSV形式で出力する
    # -----------------
    def export_total_sales(self, total_sales:int, output_path: str) -> None:
        self.logger.info("総合売上の出力を開始します")
        #with 構文は処理が終わると自動でファイルを閉じる
        #fは開いたファイル
        with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
            #csv.writer を使って、CSVに書き込むための「ライター」オブジェクトを作る
            sales_writer = csv.writer(csv_file)
            
            #ヘッダー行の作成
            #writerow() が「必ずリストを渡す」というルール
            sales_writer.writerow([CSV_HEADERS["metric"], CSV_HEADERS["value"]])
            
            #データ行を書き込む ※実際の売上
            sales_writer.writerow([REPORT_LABELS["total_sales"],total_sales])
            
        self.logger.info("総合売上CSVの出力を完了しました")
            

    # -----------------
    # 2つ目のフロー：平均売上表示
    # ・AnalyzerFlowで計算した平均売上を受け取る
    # ・平均売上をCSV形式で出力する
    # -----------------
    def export_average_sales(self,average_sales: float, output_path:str ) ->None:
        self.logger.info("平均売上の出力を開始します")
        
        #追記モード("a")で開く ※ヘッダーはかかない
        with open(output_path,mode="a" ,newline="",encoding="utf-8") as csv_file:
            sales_writer = csv.writer(csv_file)
            
            #average_salesの行を追記する
            sales_writer.writerow([REPORT_LABELS["average_sales"], average_sales])
            
        self.logger.info("平均売上CSVの出力を完了しました")

    # -----------------
    # 3つ目のフロー：商品別売上表示 
    # ・商品別売上データを受け取る
    # ・商品ごとの売上を一覧表示する
    # ・item_sales_summary = {"商品A": 100000, "商品B": 200000}
    # -----------------
    
    def export_item_sales_summary(self, item_sales_summary: dict[str, float], output_path: str) ->None:
        self.logger.info("商品別売上の出力を開始します")
        
        #追記モード
        with open(output_path, mode="a", newline="", encoding="utf-8") as csv_file:
            #csvモジュールのwriter機能でライターを作る
            sales_writer = csv.writer(csv_file)
            
            #sales_by_itemを追記する 作ったライターの.writerow()で行を書く
            #.items() を呼ぶとタプルが生まれる
            for item_name, item_sales in item_sales_summary.items():
                sales_writer.writerow([item_name, item_sales])
            
        self.logger.info("商品別売上の出力を完了しました")
            
            
    # -----------------
    # 4つ目のフロー：最高売上表示 
    # ・最高売上データを受け取る
    # ・最も売上が高いデータを表示する
    # -----------------
    def export_max_sales_record(self, max_sales_record:dict[str, int] ,output_path:str) ->None:
        self.logger.info("最高売上の出力を開始します")
        
        with open(output_path, mode="a", newline="",encoding="utf-8") as csv_file:
            #csvモジュールのwriter機能でライターを作る
            sales_writer = csv.writer(csv_file)
            
            for item_name, item_sales  in max_sales_record.items():
                sales_writer.writerow([REPORT_LABELS["max_item"],item_name])
                sales_writer.writerow([REPORT_LABELS["max_sales"],item_sales])
            
        self.logger.info("最高売上の出力を完了しました")

    # -----------------
    # 5つ目のフロー：最低売上表示
    # ・最低売上データを受け取る
    # ・最も売上が低いデータを表示する
    # -----------------
    def export_min_sales_record(self, min_sales_record:dict[str,int], output_path: str) ->None:
        self.logger.info("最低売上の出力を開始します")
        
        with open(output_path, mode="a" , newline="" , encoding= "utf-8") as csv_file:
            #CSVモジュールでwriter機能でライターを作る
            sales_writer = csv.writer(csv_file)
            for item_name, item_sales in min_sales_record.items():
                sales_writer.writerow([REPORT_LABELS["min_item"],item_name])
                sales_writer.writerow([REPORT_LABELS["min_sales"],item_sales])
            
        self.logger.info("最低売上の出力を完了しました")
        
# =========================================
# 動作確認用テスト実行
# =========================================


if __name__ == "__main__":
    #クラスを生成
    report_flow = ReportFlow()
    
    # テスト用データ（ベタ書き）
    # 1つ目
    total_sales = 2150  # int

    # 2つ目
    average_sales = 430.0  # float

    # 3つ目
    item_sales_summary = {
        "apple": 1200,
        "orange": 500,
        "banana": 450
    }  # dict[str, int]

    # 4つ目
    max_sales_record = {"apple": 700}

    # 5つ目
    min_sales_record = {"orange": 200}

    
    report_file_path = output_path()
    
    #１つ目:総売上CSV出力
    report_flow.export_total_sales(total_sales, report_file_path)
    
    #2つ目：平均売上表示
    report_flow.export_average_sales(average_sales, report_file_path)
    
    #3つ目：商品別売上表示 
    report_flow.export_item_sales_summary(item_sales_summary, report_file_path)
    
    #４つ目：最高売上表示
    report_flow.export_max_sales_record(max_sales_record , report_file_path)
    
    #5つ目：最低売上表示
    report_flow.export_min_sales_record(min_sales_record , report_file_path)
    