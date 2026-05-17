import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utils.logger import SimpleLogger

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
        with open(output_path, mode="w", newline="", encoding="utf = 8") as csv_file:
            #csv.writer を使って、CSVに書き込むための「ライター」オブジェクトを作る
            sales_writer = csv.writer(csv_file)
            
            #ヘッダー行の作成
            sales_writer.writerow(["total_sales"])
            
            #データ行を書き込む ※実際の売上
            sales_writer.writerow([total_sales])
            
        self.logger.info("総合売上CSVの出力を完了しました")
            

# -----------------
# 2つ目のフロー：平均売上表示
# ・AnalyzerFlowで計算した平均売上を受け取る
# ・平均売上をコンソールへ表示する
# -----------------

# -----------------
# 3つ目のフロー：商品別売上表示
# ・商品別売上データを受け取る
# ・商品ごとの売上を一覧表示する
# -----------------

# -----------------
# 4つ目のフロー：最高売上表示
# ・最高売上データを受け取る
# ・最も売上が高いデータを表示する
# -----------------

# -----------------
# 5つ目のフロー：最低売上表示
# ・最低売上データを受け取る
# ・最も売上が低いデータを表示する
# -----------------