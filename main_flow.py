

#読み込んだデータを分析する責務
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#各クラスをインポート
from src.loader import LoaderFlow
from src.analyzer import AnalyzerFlow
from src.reporter import ReportFlow
from src.chart import ChartFlow

#reportの保存先のパスを取得するためのヘルパーパス
from utils.helper_path import output_path

from utils.logger import SimpleLogger


class MainFlow:
    def __init__(self):
        self.logger_setup = SimpleLogger()
        self.logger = self.logger_setup.get_logger()
        
    # ========= 1つ目のフロー：CSVデータ読み込み・整形 =========
    # ・helper_path.py でファイルパスを取得する
    # ・data/sales.csv の存在チェックをする
    # ・CSVを読み込む
    # ・sales を str → int に型変換する
    # （担当：loader.py / helper_path.py）
    def run_load(self):
        self.logger.info("データの読み込みを開始します")
        
        #LoaderFlowのインスタンスを作成する
        loader = LoaderFlow()
        
        #ファイルパスを取得し、存在をチェック
        csv_file_path = loader.get_file_path()
        loader.check_file_exists(csv_file_path)
        
        #CSVを読み込む
        sales_records = loader.load_csv(csv_file_path)
        formatted_sales = loader.format_sales_data(sales_records)
        
        self.logger.info("データの読み込みが完了しました")
        return formatted_sales


    # ========= 2つ目のフロー：売上分析 =========
    # ・総売上・平均売上を計算する
    # ・商品別売上を集計する
    # ・最高売上商品・最低売上商品を特定する
    # ・分析結果を1つの辞書にまとめる
    # （担当：analyzer.py）
    def run_analyze(self,formatted_sales_records):
        self.logger.info("売上分析を開始します")
        
        #AnalyzerFlowのインスタンスを作成
        analyzer = AnalyzerFlow()
        
        #総売上・平均売上を計算する
        total_sales = analyzer.calculate_total_sales(formatted_sales_records)
        average_sales = analyzer.calculate_average_sales(formatted_sales_records)
        
        #商品別集計をしてから最高・最低を特定する
        item_sales_summary = analyzer.summarize_sales_by_item(formatted_sales_records)
        max_sales_record = analyzer.get_max_sales_record(item_sales_summary)
        min_sales_record = analyzer.get_min_sales_record(item_sales_summary)
        
        #分析結果を１つの辞書にまとめる
        analysis_result = analyzer.build_analysis_result(total_sales, average_sales ,max_sales_record, min_sales_record, item_sales_summary)
        
        self.logger.info("売上分析が完了しました")
        return analysis_result

    # ========= 3つ目のフロー：レポートCSV出力 =========
    # ・output/ に日付付きCSVファイルを作成する
    # ・総売上・平均売上・商品別売上・最高売上・最低売上を書き込む
    # （担当：reporter.py / helper_path.py）
    def run_reporter(self, analysis_result):
        self.logger.info("レポートの出力を開始します")
        
        #ReportFlowのインスタンスを作成
        reporter = ReportFlow()
        
        #日付付きのCSV保存先パスを取得する
        report_file_path = output_path()
        
        #各データをCSVに書き込みする
        reporter.export_total_sales(analysis_result["total_sales"],report_file_path)
        reporter.export_average_sales(analysis_result["average_sales"],report_file_path)
        reporter.export_item_sales_summary(analysis_result["item_sales_summary"],report_file_path)
        reporter.export_max_sales_record(analysis_result["max_sales_record"],report_file_path)
        reporter.export_min_sales_record(analysis_result["min_sales_record"],report_file_path)
        
        self.logger.info("レポートの出力が完了しました")


    # ========= 4つ目のフロー：グラフ作成 =========
    # ・商品別売上の棒グラフを作成する
    # ・output/ に日付付きPNGファイルとして保存する
    # （担当：chart.py / helper_path.py）
    def run_chart(self, analysis_result):
        self.logger.info("グラフの作成を開始します")
        
        #ChartFlowのインスタンスを作成する
        chart = ChartFlow()
        
        #商品売上の棒グラフを作成・保存する
        chart.create_bar_chart(analysis_result["item_sales_summary"])
        
        self.logger.info("グラフ作成が完了しました")
        
        
    # -----------------
    # 全フローをまとめて実行する
    # -----------------
    def run(self):
        self.logger.info("前処理を開始します")
        
        formatted_sales = self.run_load()
        analysis_result = self.run_analyze(formatted_sales)
        self.run_reporter(analysis_result)
        self.run_chart(analysis_result)