#読み込んだデータを分析する責務
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.logger import SimpleLogger
#==========================================

class AnalyzerFlow:
    def __init__(self):
        #logger
        self.logger_setup = SimpleLogger()
        self.logger = self.logger_setup.get_logger()
    
    # -----------------
    # 1つ目のフロー：売上合計を計算する
    # ・整形済みの売上データ一覧を受け取る
    # ・1件ずつ sales（売上）を取り出す
    # ・すべての売上を合計する
    # ・合計金額を返す
    # -----------------
    def calculate_total_sales(self,formatted_sales_records:list[dict[str,str|int]]) -> int:
        self.logger.info("売上合計の計算を開始します")
        
        #合計初期値
        total_sales = 0
        
        #1件ずつ加算
        for record in formatted_sales_records:
            total_sales += record["sales"]
            
        self.logger.info(f"売上合計の計算完了:{total_sales}円")
        
        return total_sales
    

    # -----------------
    # 2つ目のフロー：平均売上を計算する
    # ・整形済みの売上データ一覧を受け取る
    # ・売上合計 ÷ 件数 で平均を求める
    # ・0件の場合はエラーにならないよう考慮する
    # ・平均売上を返す
    # -----------------
    # #floatの型ヒントは平均値は小数点で返すから
    def calculate_average_sales(self, formatted_sales_records: list[dict[str,str|int]]) -> float:
        self.logger.info("平均売上の計算を開始します")
        
        #件数を取得
        records_count = len(formatted_sales_records)
        
        #0件チェック！０件の可能性も考える
        if records_count == 0:
            self.logger.info("売上データが0件です")
            return 0
        
        #合計を計算
        total_sales = 0
        
        for record in formatted_sales_records:
            total_sales += record["sales"]
            
        #平均計算
        average_sales = total_sales / records_count
        
        #.2fは小数点第２まで
        self.logger.info(f"平均売上の計算完了:{average_sales:.2f}円")
        
        return average_sales
        
        
    # -----------------
    # 3つ目のフロー：最大売上データを取得する
    # ・商品別集計データ一覧を受け取る
    # ・sales（売上）が最も大きいデータを探す
    # ・最大売上の1件分データを返す
    # -----------------
    def get_max_sales_record(self,item_sales_summary: dict[str, int]) ->dict[str, int]:
        self.logger.info("最大売上データの取得を開始します")
        
        # 0件チェック
        # データが1件もない場合は最大売上を求められないため、
        # 空の辞書を返して呼び出し元へ「該当データなし」を伝える
        if len(item_sales_summary) == 0:
            self.logger.info("売上データが０件です")
            #０件だった場合は空の辞書を返す
            return {}
        
        #最大売上を取得する
        # item_sales_summary のキー（商品名）を比較して最大の商品名を取り出す
        # max() に dict を渡すとキーを返してくれる
        max_item = max(item_sales_summary, key = lambda item: item_sales_summary[item])
        
        self.logger.info(f"最大売上取得完了:{max_item}{item_sales_summary[max_item]:}円")
        return {max_item: item_sales_summary[max_item]}
    
    # -----------------
    # 4つ目のフロー：最低売上データを取得する
    # ・整形済みの売上データ一覧を受け取る
    # ・sales（売上）が最も低いデータを探す
    # ・最低売上の1件分データを返す
    # -----------------
    def get_min_sales_record(self,item_sales_summary: dict[str, int]) ->dict[str,int]:
        self.logger.info("最低売上データの取得を開始します")
        
        # 0件チェック
        # データが1件もない場合は最低売上を求められないため、
        # 空の辞書を返して呼び出し元へ「該当データなし」を伝える
        if len(item_sales_summary) == 0:
            self.logger.info("売上データが０件です")
            #０件だった場合は空の辞書を返す
            return {}
        
        #最低売上を取得する
        #min関数を利用しているが、辞書のどれを比較するの基準値でkey = で基準値salesと教えている
        min_item = min(item_sales_summary, key= lambda item: item_sales_summary[item])
        
        self.logger.info(f"最低売上取得完了:{min_item}{item_sales_summary[min_item]:}円")
        return {min_item: item_sales_summary[min_item]}
        
    # -----------------
    # 5つ目のフロー：商品ごとの売上を集計する
    # ・整形済みの売上データ一覧を受け取る 
    # ・item（商品名）ごとに売上をまとめる
    # ・同じ商品があれば売上を加算する
    # ・商品別の集計結果を辞書で返す
    # -----------------
    def summarize_sales_by_item(self,formatted_sales_records: list[dict[str, str | int]]) -> dict[str,int]:
        self.logger.info("商品別売上集計を開始します")
        
        #集計用の空辞書
        item_sales_summary: dict[str, int] = {}
        
        #1件ずつ処理をする
        for record in formatted_sales_records:
            item = record["item"]
            sales = record["sales"]
            
            #初登場の商品なら０円で作る
            #辞書は同じキーを2個持てない
            if item not in item_sales_summary:
                item_sales_summary[item] = 0
                
            #売上を加算
            item_sales_summary[item] += sales
            
        self.logger.info(f"商品売上集計完了:{len(item_sales_summary)}商品")
        
        return item_sales_summary    


    # -----------------
    # 6つ目のフロー：分析結果をまとめる
    # ・1つ目〜4つ目の結果を受け取る
    # ・分析結果を1つの辞書にまとめる
    # ・reporter.pyへ渡しやすい形に整える
    # -----------------
    def build_analysis_result(self, total_sales:int , average_sales: float, max_sales_record:dict[str,str|int],min_sales_record:dict[str,str|int] ,item_sales_summary:dict[str,int]) -> dict:
        self.logger.info("分析結果のまとめ処理をします")
        
        #分析結果を１つの辞書にまとめる
        analysis_result = {
            "total_sales": total_sales,
            "average_sales": average_sales,
            "max_sales_record": max_sales_record,
            "item_sales_summary": item_sales_summary,
            "min_sales_record": min_sales_record
        }
        
        self.logger.info("分析結果のまとめ処理が完了しました")
        return analysis_result
"""
# =========================================
# 動作確認用テスト実行
# =========================================
if __name__ == "__main__":
    #クラスを生成
    analyzer_flow = AnalyzerFlow()
    
    # テスト用データ（ベタ書き）
    formatted_sales_records = [
        {"date": "2026-05-01", "item": "apple", "sales": 500},
        {"date": "2026-05-02", "item": "banana", "sales": 300},
        {"date": "2026-05-03", "item": "apple", "sales": 200},
        {"date": "2026-05-04", "item": "orange", "sales": 100},
    ]
    
    #①売上合計を計算
    total_sales = analyzer_flow.calculate_total_sales(formatted_sales_records)
    print("合計金額:",total_sales)
    
    #②平均売上
    average_sales = analyzer_flow.calculate_average_sales(formatted_sales_records)
    print("平均売上:",average_sales)
    
    #⑤商品別売上
    item_sales_summary = analyzer_flow.summarize_sales_by_item(formatted_sales_records)
    print("商品別集計:", item_sales_summary)
    
    
    #③最大売上
    max_sales_record = analyzer_flow.get_max_sales_record(item_sales_summary)
    print("最大売上:", max_sales_record)
    
    #④最低売上
    min_sales_record = analyzer_flow.get_min_sales_record(item_sales_summary)
    print("最低売上:", min_sales_record)
    

    #まとめ
    analysis_result = analyzer_flow.build_analysis_result(total_sales,average_sales,max_sales_record,min_sales_record,item_sales_summary)
    print("分析結果:", analysis_result)
    
"""