#読み込んだデータを分析する責務
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

#matplotlib.pyplot はグラフ描画の機能をまとめたモジュール
import matplotlib.pyplot as plt

from utils.logger import SimpleLogger
from utils.helper_path import chart_path

#=============================================

class ChartFlow:
    def __init__(self):
        self.logger_setup = SimpleLogger()
        self.logger = self.logger_setup.get_logger()
        
# -----------------
# 1つ目のフロー：棒グラフ作成・保存
# ・商品別売上データ（item_sales_summary）を受け取る
# ・商品名をX軸、売上額をY軸に設定する
# ・タイトル・軸ラベルを設定する
# ・棒グラフを描画する
# ・output/ に日付付きPNGファイルとして保存する
# -----------------

    def create_bar_chart(self, item_sales_summary: dict[str, int]) -> None:
        self.logger.info("棒グラフの作成を開始します")
        
        #日本語フォントを設定する
        plt.rcParams['font.family'] = 'Hiragino Sans'
        
        #売上の高い順に並べ変える
        sorted_summary = dict(sorted(item_sales_summary.items(), key = lambda x: x[1], reverse = True))
        #      ↑                            ↑                   ↑
        #  タプルの一覧を渡す            比較する基準          降順（高い順）
        #  [("ノートパソコン", 860000),   x[1] = 売上額        Falseにすると昇順
        #   ("スマートフォン", 598000),
        #   ...]

        
        # X軸（商品名）とY軸（売上額）のデータをリストで取り出す
        item_names = list(sorted_summary.keys())
        item_sales = list(sorted_summary.values())
        
        # グラフ全体のサイズを設定する(横8インチ、縦5インチ)
        plt.figure(figsize=(8,5))
        
        #棒グラフを作成する(データを渡す)
        plt.bar(item_names, item_sales)
        # ha = horizontal alignment（水平方向の揃え位置）の略
        # 'right' → ラベルの右端を目盛りの位置に合わせる
        # これがないと、傾けたときにラベルがずれて見た目が悪くなる
        plt.xticks(rotation = 45, ha = 'right')
        
        #タイトルを設定
        plt.title("商品別売上")
        
        # X軸とY軸のラベルを設定する
        plt.xlabel("商品名")
        plt.ylabel("売上額(円)")
        
        #グラフの各要素（タイトル・軸ラベル・X軸のラベル）が画像の外にはみ出して切れないように余白を自動調整
        plt.tight_layout()
        
        # 保存先のパスを取得する
        chart_file_path = chart_path()
        
        # PNGファイルとして保存する
        plt.savefig(chart_file_path)
        
        #グラフを閉じてメモリを解放する
        plt.close()
        
        self.logger.info("棒グラフの作成が完了しました")

"""      
# =========================================
# 動作確認用テスト実行
# =========================================
if __name__== "__main__":
    #インスタンス作成
    chart_flow = ChartFlow()
    
    # テスト用データ（ベタ書き）
    item_sales_summary = {
        "apple": 1200,
        "orange": 500,
        "banana": 450
    }
    
    chart_flow.create_bar_chart(item_sales_summary)
"""