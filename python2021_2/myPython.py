import os
import shutil
import datetime
import glob


def createWorkDir(srcDir):

    # ディレクトリをまるごと別ディレクトリとして同階層にコピー。名前は指定のディレクトリ+_実行日時。
    dstDir = srcDir + '_' + datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    shutil.copytree(srcDir, dstDir)
    return dstDir


def main(srcDir):

    # ディレクトリをまるごと別ディレクトリとして同階層にコピー。名前は指定のディレクトリ+_実行日時。
    dstDir = createWorkDir(srcDir)

    # お掃除 : 「bk」ディレクトリは削除。
    ls = glob.glob(dstDir + '\\**\\bk', recursive=True)
    for l in ls:
        print(l)
        shutil.rmtree(l)

    # 「.xlsx」をzipにして別名保存 : これやるかどうか微妙


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルのところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(os.getcwd())

    # さぁがんばろう
    main('20210930_エクセルをMDに')

    print('★End - PG')

# 以下自分用のメモ帳

# 006BA135 DBの緑色の色コード
