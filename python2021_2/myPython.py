import os   # カレントディレクトリ変更で使用
import shutil   # ディレクトリコピーに使用
import datetime  # 保存時の日付情報で使用
import glob  # エクセル一覧の取得で使用

import openpyxl  # エクセル操作。要「pip install openpyxl」。ちなみに端末内にエクセルがインストールされていなくても動く。

srcDir = ""  # インプットディレクトリ
dstDir = ""  # アウトプットディレクトリ


class pageData:

    def __init__(self):
        self.title = ""  # タイトル
        self.history = []   # 履歴
        self.layout = {}    # レイアウト : 概要となんか
        self.layoutItems = []  # 画面項目
        self.inputItems = []  # 入力項目
        self.events = []    # イベント一覧
        self.inputCheck = []    # 入力チェック
        self.businessCheck = []  # 業務チェック

    def setData(self, data):
        pass


def createWorkDir():

    # print('★★★ createWorkDir')

    # ディレクトリをまるごと別ディレクトリとして同階層にコピー。名前は指定のディレクトリ+_実行日時。
    global dstDir
    dstDir = srcDir + '_' + datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    shutil.copytree(srcDir, dstDir)


def init():

    print('★★ 初期化処理')

    # ディレクトリをまるごと別ディレクトリとして同階層にコピー。名前は指定のディレクトリ+_実行日時。
    createWorkDir()

    # お掃除 : 「bak」ディレクトリは削除。
    print('★★★ 削除ディレクトリ一覧')
    ls = glob.glob(dstDir + '\\**\\bak', recursive=True)
    for l in ls:
        print(l)
        try:
            shutil.rmtree(l)
            continue

        except FileNotFoundError:
            continue

    # 「.xlsx」をzipにして別名保存 : これやるかどうか微妙


def readExcel(title, wb):

    d = pageData()  # インスタンス化

    d.title = title  # タイトル設定

    # 改訂履歴読み込み
    ws = wb['改訂履歴']
    row = 5  # 行カーソル。とりあえずデータ開始行を当てにいく。行数5に頼らずに出てくるまでを探索もできるけど面倒くさい
    col = 2  # 列カーソル。2 は 版数の列。項番の1は値が入っているので今回は使えない。一番下まで行っちゃうから。

    while ws.cell(row, col).value != None:  # 空っぽの版数があるうちはループする。なければループ終わり。
        d.history.append([ws.cell(row, n).value for n in range(1, 8)])  # クラスのhistoryに項番 ～ 改定理由 を取り込む。
        row = row + 1

    # レイアウト読み込み
    ws = wb['レイアウト']
    row = col = 1   # 行カーソルと列カーソルをセルの「A1」で初期化。ここから下に探索する。

    # 概要欄探索
    while ws.cell(row, col).value != '概要':
        row = row + 1
    d.layout = {'Overview': ws.cell(row + 1, col).value}    # 概要欄ゲット

    # 改訂履歴読み込み
    ws = wb['画面項目']
    row = col = 1   # 行カーソルと列カーソルをセルの「A1」で初期化。ここから下に探索する。

    # データタイトル探索
    while ws.cell(row, col).value != '項番':
        row = row + 1

    row = row + 1   # データ部へ移動。項番の下はデータ部が即開始するようにPMO確認済み。

    while ws.cell(row, col).value != None:  # 空っぽの版数があるうちはループする。なければループ終わり。
        d.layoutItems.append([ws.cell(row, n).value for n in range(1, 17)])  # この行を、列の右端まで取り込む。
        row = row + 1

    print('ok')


def exec():
    print('\n★★ 本処理')

    # エクセルファイルの一覧を取得
    ls = glob.glob(dstDir + '\\*画面設計書\\**\\*.xlsx', recursive=True)
    # 一つだけデバッグ用。要らんときはコメントアウトするなり。
    ls = [dstDir + '\\06.画面設計書\\共通\\画面設計書_セッションタイムアウト.xlsx']
    for l in ls:
        wb = openpyxl.load_workbook(l, data_only=True)  # ファイル読み込み

        d = readExcel(l[l.rfind('_')+1: l.rfind('.')], wb)  # エクセル読み込み


def main():

    # 初期化 作業用ディレクトリにコピーしたり bakのお掃除とか
    # init()

    # エクセル読み込む
    exec()


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルのところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('- カレントディレクトリ : ' + os.getcwd())

    # さぁがんばろ
    dstDir = srcDir = '20210930_エクセルをMDに2'
    main()

    print('★End - PG')

# 以下自分用のメモ帳

# 006BA135 DBの緑色の色コード
