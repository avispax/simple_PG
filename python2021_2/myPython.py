import os   # カレントディレクトリ変更で使用
import shutil   # ディレクトリコピーに使用
import datetime  # 保存時の日付情報で使用
import glob  # エクセル一覧の取得で使用

import openpyxl  # エクセル操作。要「pip install openpyxl」。ちなみに端末内にエクセルがインストールされていなくても動く。

from concurrent.futures import ThreadPoolExecutor

srcDir = ""  # インプットディレクトリ。元ネタ。作業用ディレクトリ作成時に、最初の1回だけ参照する。
workDir = "work"  # 作業用ディレクトリ。bakや作成中のディレクトリを削除。ここのエクセルを読み込んで、markdownを生成する。
dstDir = ""  # アウトプットディレクトリ。ここにmdを生成する。
isSkipInit = False    # 初期化処理（init()）を実行するかどうか。スキップする場合（True）、work ディレクトリ とかを毎回やらない。めんどくさい人用。


class screenDesignData:
    def __init__(self):
        self.title = ""  # タイトル
        self.history = []   # 履歴
        self.layout = {}    # レイアウト : 概要となんか
        self.layoutItems = []  # 画面項目
        self.inputItems = []  # 入力項目
        self.events = []    # イベント一覧
        self.inputCheck = []    # 入力チェック
        self.businessCheck = []  # 業務チェック
        self.functions = {}  # 機能設計群

        # Markdown定型文
        self.markdownTemplate = ('# イトーヨーカドーネットスーパー<br><br>@specTitle 画面設計書\n'
                                 '\n'
                                 'ver.@specVersion\n'
                                 '\n'
                                 '株式会社ビッグツリーテクノロジー＆コンサルティング\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 改訂履歴\n'
                                 '\n'
                                 '@specHistory'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 概要\n'
                                 '\n'
                                 '```Overview\n'
                                 '@specOverview\n'
                                 '```\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## レイアウト\n'
                                 '\n'
                                 '  - 画面タイトル1  \n'
                                 '    ![画面1](img/1.jpg)\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 画面項目\n'
                                 '\n'
                                 '@specLayoutItems'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## イベント一覧\n'
                                 '\n'
                                 '@specEvents'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 入力チェック\n'
                                 '\n'
                                 '- 入力チェック  \n'
                                 '\n'
                                 '@specInputCheck'
                                 '\n'
                                 '- 業務チェック  \n'
                                 '\n'
                                 '@specBusinessCheck'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 機能\n'
                                 '\n'
                                 '@functions'
                                 )

        self.markdownTemplate_functions = ('### @name\n'
                                           '\n'
                                           '- id : @id\n'
                                           '\n'
                                           '#### 入力\n'
                                           '\n'
                                           '@input\n'
                                           '\n'
                                           '#### 出力\n'
                                           '\n'
                                           '@output\n'
                                           '\n'
                                           '#### 処理内容\n'
                                           '\n'
                                           '```\n'
                                           '@processDetail'
                                           '```\n'
                                           '\n'
                                           )

    def generateMarkdown(self):

        # バージョン情報を履歴情報から取得。一番最後の配列の2番目の要素を固定で取得。
        version = self.history[len(self.history) - 1][1]

        # マークダウン用の文字列を生成
        outputStr = (self.markdownTemplate
                     .replace('@specTitle', self.title)
                     .replace('@specVersion', str('{:.2f}'.format(round(version, 2))))  # バージョンは「##.##」の形式になるように四捨五入とフォーマットをカマす。
                     .replace('@specHistory', arrayToMarkdownTable(self.history, '改訂履歴'))
                     .replace('@specOverview', self.layout['Overview'])
                     .replace('@specLayoutItems', arrayToMarkdownTable(self.layoutItems, '画面項目'))
                     .replace('@specEvents', arrayToMarkdownTable(self.events, 'イベント一覧'))
                     .replace('@specInputCheck', arrayToMarkdownTable(self.inputCheck, '入力チェック'))
                     .replace('@specBusinessCheck', arrayToMarkdownTable(self.businessCheck, '業務チェック'))
                     .replace('@functions', self.generateFunctions())
                     )

        return outputStr

    def generateFunctions(self):
        returnStr = ''
        sorted_functions = sorted(self.functions.items(), key=lambda x: x[0])
        for k, v in sorted_functions:    # キーでソートしながら中身を取り出す。sheetNamesはシートの並び順だが、dictの順序が保証されてるか怪しかったので。
            returnStr = returnStr + (self.markdownTemplate_functions
                                     .replace('@name', v['name'])
                                     .replace('@id', str(v['id'] or ''))
                                     .replace('@input', '- ' + v['input'].replace('\n', '\n- '))
                                     .replace('@output', '- ' + v['output'].replace('\n', '\n- '))
                                     .replace('@processDetail', v['processDetail'])
                                     )
        return returnStr


class reportData:   # 帳票設計書クラス

    def __init__(self):
        self.title = ""  # タイトル
        self.history = []   # 履歴
        self.layout = {}    # レイアウト : 概要となんか
        self.reportItems = []  # 帳票項目
        self.events = []    # イベント一覧

        # Markdown定型文
        self.markdownTemplate = ('# イトーヨーカドーネットスーパー<br><br>@specTitle 帳票設計書\n'
                                 '\n'
                                 'ver.@specVersion\n'
                                 '\n'
                                 '株式会社ビッグツリーテクノロジー＆コンサルティング\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 改訂履歴\n'
                                 '\n'
                                 '@specHistory'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 概要\n'
                                 '\n'
                                 '```Overview\n'
                                 '@specOverview\n'
                                 '```\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## レイアウト\n'
                                 '\n'
                                 '  - 画面タイトル1  \n'
                                 '    ![画面1](img/1.jpg)\n'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## 帳票項目\n'
                                 '\n'
                                 '@specReportItems'
                                 '\n'
                                 '------------------------------------------------------------------------------------------\n'
                                 '\n'
                                 '## イベント一覧\n'
                                 '\n'
                                 '@specEvents'
                                 '\n'
                                 )

    def generateMarkdown(self):

        # バージョン情報を履歴情報から取得。一番最後の配列の2番目の要素を固定で取得。
        version = self.history[len(self.history) - 1][1]

        # マークダウン用の文字列を生成
        outputStr = (self.markdownTemplate
                     .replace('@specTitle', self.title)
                     .replace('@specVersion', str('{:.2f}'.format(round(version, 2))))  # バージョンは「##.##」の形式になるように四捨五入とフォーマットをカマす。
                     .replace('@specHistory', arrayToMarkdownTable(self.history, '改訂履歴'))
                     .replace('@specOverview', self.layout['Overview'])
                     .replace('@specReportItems', arrayToMarkdownTable(self.reportItems, '帳票項目'))
                     .replace('@specEvents', arrayToMarkdownTable(self.events, 'イベント一覧'))
                     )

        return outputStr


def arrayToMarkdownTable(array, sheetTitle):
    s = ''

    s = '| ' + ' | '.join(array[0]).replace('\n', '<br>') + ' |\n'    # 1配列目は項目行。これはかならず存在する。|項番|aaa|bbb|ccc|ddd|とかの。
    s = s + '|:--' * len(array[0]) + '|\n'    # 間に表のあれ（アライメント？）を入れる。|:--|:--|:--|

    for arr in array[1:]:   # ここからデータ部整形

        # 結合に向けての準備
        for col in range(len(arr)):
            if isinstance(arr[col], str):
                arr[col] = arr[col].replace('\n', '<br>')  # str 型なら 改行コード（\n）の存在に気をつけて、基本はそのまま採用。
            elif arr[col] is None:
                arr[col] = ' '    # None（値が入っていなかったセル）は「 」（半角スペース）を設定。マークダウンの表として「 」が必要なので。

            elif sheetTitle == '改訂履歴' and col == 1:  # シート「改訂履歴」専用処理。
                # なお、まれに各セルが 数値や日付 + フォーマット ではなく文字列としてそのまま書かれている状況もある。それはもうわざとやっているとみなし、先頭の分岐でそのまま採用している。
                arr[col] = str('{:.2f}'.format(round(arr[col], 2)))  # シート「改訂履歴」の2列目はフォーマット指定の版数。値と実態が異なるので変換する。
                # TODO 端数処理:切り捨て
            elif sheetTitle == '改訂履歴' and col == 2:
                arr[col] = f'{arr[col]:%Y/%m/%d}'   # 日付型をフォーマットする。「2021/01/01」形式

            else:
                arr[col] = str(arr[col]).replace('\n', '<br>')  # なんかわからないものはすべてstr型に変更する。改行コード（\n）の存在に気をつけて、基本はそのまま採用。

        # TODO : 入力チェック、業務チェックの場合はちょっと字下げをして、「- 入力チェック  」に従属するような表にする。Markdown的に。
        s = s + '| ' + ' | '.join(arr) + ' |\n'

    return s


def init():

    print('\n★★ 初期化処理 - start')

    # もし「work」があるなら削除
    try:
        shutil.rmtree('work')
    except:
        pass

    # ディレクトリをまるごと別ディレクトリとして同階層にコピー。名前は workDir のとおり。
    shutil.copytree(srcDir, workDir)

    # お掃除 : 「bak」ディレクトリは削除。
    ls = glob.glob(workDir + '\\**\\bak', recursive=True)
    for l in ls:
        print(l)
        try:
            shutil.rmtree(l)
            continue

        except FileNotFoundError:
            continue

    # お掃除 : 「作成中」ディレクトリは削除。つーかこういうのもうGitとかで管理して、完成したやつだけコミットしろや。履歴管理は履歴管理サービスに任せぇ！
    ls = glob.glob(workDir + '\\**\\*作成中', recursive=True)
    for l in ls:
        print(l)
        try:
            shutil.rmtree(l)
            continue

        except FileNotFoundError:
            continue

    # 「.xlsx」をzipにして別名保存 : これやるかどうか微妙

    print('\n★★ 初期化処理 - end')


def readSheet(ws, array):

    # まず表の開始位置（項番のセル）と表の右端を探索する。開始位置から行カーソルをwhileループする。右端まではforループで、それぞれ反復処理する。
    # 行で探索する対象の列も定義する。変数はtargetcolとする。

    r = targetcol = maxcol = 1  # それぞれの行列の変数。内容は↑の通り。

    # 表の開始位置を探索
    while ws.cell(r, 1).value != '項番':  # 「項番」は必ず列「A」に存在するので、それを目指して行カーソル（r）を進める。
        r = r + 1

    # 表の右端の列番号を探索。ただし改訂履歴は2段になってるせいでとりあえずあとで固定値でいいや。
    while ws.cell(r, maxcol).value != None:
        maxcol = maxcol + 1

    if ws.title == '改訂履歴':
        # 改訂履歴だけ項目が2段になってるから2つずらすし、列も「版数」のセルを対象とする。なんか右端に段組のセル分を調整する。
        # こいつ異フォーマットすぎて関数化しなけりゃよかった。
        r = r + 2
        targetcol = 2
        maxcol = maxcol + 3

        # ついでに項目ももうこっちで作っちゃう。他の表はセルを読んで自動取得+生成だけど、こいつめんどくさい。
        array.append(['項番', '版数', '更新日付', '更新者', '改定箇所', '改定内容', '改定理由', '機能要件承認_担当者', '機能要件承認_第三者', '非機能要件承認_担当者', '非機能要件承認_第三者'])

    while ws.cell(r, targetcol).value != None:  # 行 ： 空っぽのセルが出てくるまでループする。
        array.append([ws.cell(r, n).value for n in range(1, maxcol)])  # 列「A」から「maxcol」までを1行分の列ループ。ちなみに空のセルは「None」が入る。
        r = r + 1

        # もしも「特定の列はスキップ」という要求があれば、for 文を分解して以下のようにする。
        # for n in range(1, maxcol):
        #     if ws.cell(r, n).value == 'aaa':
        #         continue
        #     array.append(ws.cell(r, n).value)
        # r = r + 1


def readBaseSheets(wb, d):

    # 改訂履歴とレイアウトのシートを読み込む。レイアウトは概要欄だけをいったん。

    readSheet(wb['改訂履歴'], d.history)    # 改訂履歴読み込み

    # レイアウト読み込み - ここから
    ws = wb['レイアウト']
    row = col = 1   # 行カーソルと列カーソルをセルの「A1」で初期化。ここから下に探索する。

    # 概要欄探索
    while ws.cell(row, col).value != '概要':
        row = row + 1
    d.layout = {'Overview': ws.cell(row + 1, col).value}    # 概要欄ゲット
    # レイアウト読み込み - ここまで

    return d


def readExcelSheetsForScreenDesignSpec(title, wb):

    d = screenDesignData()  # インスタンス化

    d.title = title  # タイトル設定

    d = readBaseSheets(wb, d)    # 改訂履歴とレイアウトは今回の3ブックには必ず存在するので、関数化して省エネ。製造的に。

    readSheet(wb['画面項目'], d.layoutItems)    # 画面項目読み込み

    readSheet(wb['入力項目'], d.inputItems)    # 入力項目読み込み

    readSheet(wb['イベント一覧'], d.events)    # イベント一覧読み込み

    readSheet(wb['入力チェック'], d.inputCheck)    # 入力チェック読み込み

    readSheet(wb['業務チェック'], d.businessCheck)    # 業務チェック読み込み

    # 【機能】xxx シート読み込み - ここから
    for i, s in enumerate(wb.sheetnames):

        # ガード節 : シート名に「【機能】」がなければスキップ
        if '【機能】' not in s:
            continue

        # 読み込み開始
        ws = wb[s]  # シートをちゃんと読み込み。

        # 変数とか準備
        row = col = maxrow = maxcol = 1
        data = {}
        while ws.cell(maxrow, 1).value != '★END':  # end位置（下端）を特定
            maxrow = maxrow + 1
            if maxrow > 500:   # これぐらい到達しなかったらもうそこまででいいよ
                break

        while ws.cell(1, maxcol).value != '★END':  # end位置（右端）を特定
            maxcol = maxcol + 1
            if maxcol > 100:    # これぐらい到達しなかったらもうそこまででいいよ
                break

        # 機能IDと機能名
        while ws.cell(row, 1).value != '機能ID':    # 機能名と機能IDが存在する行まで行カーソルを移動
            row = row + 1

        data['id'] = ws.cell(row + 1, 1).value    # 機能IDを取得

        while ws.cell(row, col).value != '機能名':  # 機能名が存在する列まで列カーソルを移動
            col = col + 1

        data['name'] = ws.cell(row + 1, col).value  # 機能名を取得

        # 入力と出力
        col = 1
        while ws.cell(row, 1).value != '入力':    # 行カーソル移動
            row = row + 1

        data['input'] = ws.cell(row + 1, 1).value    # 入力の内容を取得

        while ws.cell(row, col).value != '出力':  # 列カーソル移動
            col = col + 1

        data['output'] = ws.cell(row + 1, col).value  # 出力の内容を取得

        # 処理内容
        col = 1
        while ws.cell(row, 1).value != '繰返':    # 行カーソル移動
            row = row + 1

        values = []
        for rowdata in ws.iter_rows(min_row=row+1, max_row=maxrow, min_col=3, max_col=maxcol):  # 行の内容を指定の範囲で 1セルずつ取得。数値とかが入ってても困るので文字列にキャストする。
            values.append([str(cell.value) if cell.value is not None else ' ' for cell in rowdata])

        processDetail = ''
        for v in values:
            processDetail = processDetail + ''.join(v).rstrip() + '\n'  # 1行としておかしくない感じにトリムしたり改行コードであれしたりと、全体で1文になるように操作

        data['processDetail'] = processDetail

        d.functions[i] = data   # クラスに追加

    # 【機能】xxx シート読み込み - ここまで

    return d


def readExcelSheetsForReportSpec(title, wb):
    d = reportData()  # インスタンス化

    d.title = title  # タイトル設定

    d = readBaseSheets(wb, d)    # 改訂履歴とレイアウトは今回の3ブックには必ず存在するので、関数化して省エネ。製造的に。

    readSheet(wb['帳票項目'], d.reportItems)    # 帳票項目読み込み

    readSheet(wb['イベント一覧'], d.events)    # イベント一覧読み込み

    return d


def convertThread(l):

    # エクセルブックを開いて、シートをクラスに読み込んで、配置用ディレクトリを作って、mdを生成する。
    # 読み込み関数は関数オブジェクトとして渡してもらう

    print(l)
    wb = openpyxl.load_workbook(l, data_only=True)  # ファイル読み込み

    # 各設計書用の読み込み関数を関数オブジェクトとして利用する。
    func = None
    fileName = os.path.basename(l)
    if '画面設計書_' in l:
        func = readExcelSheetsForScreenDesignSpec
    elif '帳票設計書_' in l:
        func = readExcelSheetsForReportSpec
    else:
        print('■ error - noFunc : ' + l)

    d = None
    try:
        d = func(l[l.rfind('_')+1: l.rfind('.')], wb)  # エクセルの各シート読み込み
    except:
        print('■ error : ' + l)
        return

    # アウトプット準備 : ディレクトリ作成
    dirPath = l.replace(workDir, dstDir)    # work のままなのでアウトプットディレクトリにリネーム。
    fileName = os.path.splitext(os.path.basename(l))[0].rstrip()  # ファイル名（拡張子なし）
    dirPath = os.path.dirname(dirPath) + os.sep + fileName  # ↑のファイル名を付与したディレクトリにする。階層深くなるけどそういうもの。
    os.makedirs(dirPath + os.sep + 'img', exist_ok=True)    # img の階層まで一気にディレクトリ作成

    # md生成
    outputFileName = dirPath + os.sep + fileName + '.md'
    with open(outputFileName, mode='w', encoding='utf-8_sig') as f:
        # for s in md:
        f.write(d.generateMarkdown() + '\n')


def exec():
    print('\n★★ 本処理 - start')

    # エクセルファイルの一覧を取得（or 指定）して順次読み込み。なんにせよリスト型になってればOK

    # まずは画面設計書
    ls = glob.glob(workDir + '\\*画面設計書\\**\\*.xlsx', recursive=True)
    # ls = [
    #     'work\\06.画面設計書\\共通パーツデザイン\\画面設計書_SC02-03-01_共通パーツデザイン（値引対象）.xlsx'
    # ]
    # ls = ['work\\画面設計書_機能設計_サンプル.xlsx']

    # 次に帳票設計書
    # ls = glob.glob(workDir + '\\*帳票設計書\\**\\*.xlsx', recursive=True)
    # ls = ls + ['work\\15.帳票設計書\\店舗管理\\商品管理\\0019_【機密(Ａ)】【新お届け】帳票設計書_チラシ商品 Soldout表示リスト .xlsx',
    #            'work\\15.帳票設計書\\店舗管理\\精算管理\\0001_【機密(Ａ)】【新お届け】帳票設計書_ネットスーパー売上集計表.xlsx',
    #            'work\\15.帳票設計書\\店舗管理\\集荷管理\\0002_【機密(Ａ)】【新お届け】帳票設計書_お客様メモ.xlsx']

    # 作業開始
    with ThreadPoolExecutor(max_workers=6) as pool:
        pool.map(convertThread, ls)

    # メール設計書

    print('\n★★ 本処理 - end')


def main():

    # 初期化 作業用ディレクトリにコピーしたり bakのお掃除とか
    if not isSkipInit:  # スキップしない場合は init() 実施。あまり負荷ではないが、ワークディレクトリの削除とコピーを行っているので、ソースディレクトリが変わってないならやんなくてよい。プログラムの初実行とソースの設計書が変わったらやってね。
        init()

    # エクセル読み込む
    exec()


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルが存在するところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('- カレントディレクトリ : ' + os.getcwd())

    # さぁがんばろ
    srcDir = '20210930_エクセルをMDに'  # 元ネタが存在するディレクトリを指定。Dropbox上でもいいけど、容量節約で実態がないモードにしているとたぶん動かない。素直にローカルPCのWorkとかでお願いします。
    # アウトプットディレクトリのパスを生成
    dstDir = srcDir + '_Markdown_' + datetime.datetime.today().strftime("%Y%m%d%H%M%S")

    isSkipInit = True   # 初回はかならずFalseで。2回目以降はめんどいからFalseでもよいよ。

    main()

    print('★End - PG')

# 以下自分用のメモ帳

# 006BA135 DBの緑色の色コード
