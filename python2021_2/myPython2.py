import os   # カレントディレクトリ変更で使用
import shutil   # ディレクトリコピーに使用
import glob  # エクセル一覧の取得で使用
import datetime  # 保存時の日付情報で使用
from concurrent.futures import ThreadPoolExecutor   # スレッド周り用
SOURCE_DIRECTORY = ""  # インプットディレクトリ。元ネタ。作業用ディレクトリ作成時に、最初の1回だけ参照する。
OUTPUT_DIRECTORY = ""  # アウトプットディレクトリ。ここにmdを生成する。


def copy_thread(file):

    # 現在の「style.css」を退避する。
    new_file = file.replace('style.css', 'style_old.css')
    os.rename(file, new_file)

    # カレントにある 「style.css」 を、もともとあった「style.css」としてコピーする。
    shutil.copy('style.css', file)


def modify_md_thread(file):

    s = ''
    with open(file, encoding='utf-8_sig') as f:
        s = f.read()

    # 1. タイトルをIDと名称に更新する。ファイル名をそのまま採用
    t = '# イトーヨーカドーネットスーパー<br><br>'
    pos = s.find(t) + len(t)
    pos2 = s.rfind(' ', pos, s.find('設計書', pos))
    file_name = os.path.basename(file)
    s = s.replace(s[pos:pos2], file_name[file_name.find('_') + 1: file_name.rfind('.')])

    # 2. 画面設計書のチェック項目があれば注釈をつける
    if '画面設計書_' in file:
        t1 = '### 入力チェック'
        t2 = '### 業務チェック'
        t3 = '------------------------------------------------------------------------------------------'

        pos = s.find(t1) + len(t1)
        pos2 = s.find(t2, pos)
        pos3 = s.find('- 定義なし', pos, pos2)

        if pos3 == -1:
            s = s[:pos2 - 1] + '<div class="annotation">*メッセージ表示位置画面 項目項番が「－」ハイフンの場合は共通のメッセージエリアに表示する。</div>\n\n' + s[pos2:]

        pos = s.find(t2) + len(t2)
        pos2 = s.find(t3, pos)
        pos3 = s.find('- 定義なし', pos, pos2)

        if pos3 == -1:
            s = s[:pos2 - 1] + '<div class="annotation">*メッセージ表示位置画面 項目項番が「－」ハイフンの場合は共通のメッセージエリアに表示する。</div>\n\n' + s[pos2:]

    # 3. 最後に<footer>をつける
    if s.find('<footer>以上</footer>') == -1:
        s = s + '\n<footer>以上</footer>\n'

    # 現在の「*.md」を退避する。
    new_file = file.replace('.md', '_old.md')
    os.rename(file, new_file)

    # md生成
    with open(file, mode='w', encoding='utf-8_sig') as f:
        f.write(s)


def modify_html_thread(file):

    s = ''
    with open(file, encoding='utf-8_sig') as f:
        s = f.read()

    # 1. タイトルをIDと名称に更新する。ファイル名をそのまま採用
    t = '# イトーヨーカドーネットスーパー<br><br>'
    pos = s.find(t) + len(t)
    pos2 = s.rfind(' ', pos, s.find('設計書', pos))
    file_name = os.path.basename(file)
    s = s.replace(s[pos:pos2], file_name[file_name.find('_') + 1: file_name.rfind('.')])

    # 2. 画面設計書のチェック項目があれば注釈をつける
    if '画面設計書_' in file:
        t1 = '### 入力チェック'
        t2 = '### 業務チェック'
        t3 = '------------------------------------------------------------------------------------------'

        pos = s.find(t1) + len(t1)
        pos2 = s.find(t2, pos)
        pos3 = s.find('- 定義なし', pos, pos2)

        if pos3 == -1:
            s = s[:pos2 - 1] + '<div class="annotation">*メッセージ表示位置画面 項目項番が「－」ハイフンの場合は共通のメッセージエリアに表示する。</div>\n\n' + s[pos2:]

        pos = s.find(t2) + len(t2)
        pos2 = s.find(t3, pos)
        pos3 = s.find('- 定義なし', pos, pos2)

        if pos3 == -1:
            s = s[:pos2 - 1] + '<div class="annotation">*メッセージ表示位置画面 項目項番が「－」ハイフンの場合は共通のメッセージエリアに表示する。</div>\n\n' + s[pos2:]

    # 3. 最後に<footer>をつける
    if s.find('<footer>以上</footer>') == -1:
        s = s + '\n<footer>以上</footer>\n'

    # 現在の「*.html」を退避する。
    new_file = file.replace('.html', '_old.html')
    os.rename(file, new_file)

    # md生成
    with open(file, mode='w', encoding='utf-8_sig') as f:
        f.write(s)


def main():

    # 準備
    shutil.copytree(SOURCE_DIRECTORY, OUTPUT_DIRECTORY)  # ディレクトリをまるごと別ディレクトリとして同階層にコピー。

    # スタイルシートのコピー
    def copy_style_css():
        print('- ★★ start : スタイルシートのコピー')
        # style.css の一覧を取得
        ls = glob.glob(OUTPUT_DIRECTORY + '\\**\\style.css', recursive=True)

        # コピー開始
        with ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(copy_thread, ls)
        print('- ★★ end : スタイルシートのコピー')

    def modify_markdown():
        print('- ★★ start : markdown の改造')
        # markdown の一覧を取得
        ls = glob.glob(OUTPUT_DIRECTORY + '\\**\\*.md', recursive=True)

        # 変換開始
        with ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(modify_md_thread, ls)
        print('- ★★ end : markdown の改造')

    def modify_html():
        print('- ★★ start : html の改造')
        # markdown の一覧を取得
        ls = glob.glob(OUTPUT_DIRECTORY + '\\**\\*.html', recursive=True)

        # 変換開始
        with ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(modify_html_thread, ls)
        print('- ★★ end : html の改造')

    # copy_style_css()  # 処理1 : style.css を置き換える
    # modify_markdown()   # 処理2 : markdown を改造する


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルが存在するところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('- カレントディレクトリ : ' + os.getcwd())

    SOURCE_DIRECTORY = '20210930_エクセルをMDに'  # 元ネタが存在するディレクトリを指定。Dropbox上でもいいけど、容量節約で実態がないモードにしているとたぶん動かない。素直にローカルPC上でお願いします。
    OUTPUT_DIRECTORY = 'zz_Output_' + datetime.datetime.today().strftime("%Y%m%d%H%M%S")  # アウトプットディレクトリのパスを生成

    main()

    print('★End - PG')


# 以下、自分用メモ
