
from pathlib import Path
import sys

##########################
#ルートパス取得(EXE対応)
##########################

def get_root_path():
    #getattr(オブジェクト,属性名,デフォルト値　→　あるか分からない属性を、安全に取り出す係
    #実行はexeファイルされているのか判定　sys frozenはこれってexeですか？　→　Falseではい！
    if getattr(sys, 'frozen', False):
        #executableはexeファイルの場所を返していて.parentでその親フォルダを指す
        return Path(sys.executable).parent
    
    else:
        #Pythonでの実行はこのファイルから２つ上の階層を返す
        return Path(__file__).parents[1]
    
##########################
# データ系パス
##########################
#読み込み
def data_path(file_name:str):
    return get_root_path() / "data" / file_name

#出力
def output_path():
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    return get_root_path()/"output"/ f"{today}_report.csv"

#グラフ作成
def chart_path():
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    return get_root_path()/"output" / f"{today}_chart.png"
    




##########################
# 設定・環境ファイル系
##########################
'''
def get_creds_path():
    #cread.jsonのパスを返す
    return get_root_path()/"creds.json"

def get_env_path():
    #.envのパスを返す
    return get_root_path()/".env"
'''