import difflib


class myDebug:
    debugMode = True

    def printPositions(self, current, next):
        if not self.debugMode:
            return

        # デバッグ用 : 処理位置を出力する
        print("★現在のカーソル位置（概念） : " + str(current) + "、次の区切り位置 : " + str(next))

    def printData(self, debugTitle, data):
        if not self.debugMode:
            return

        # デバッグ用 : データを出力する
        print("★" + str(debugTitle) + " : " + str(data))

    def printFree(self, s):
        if not self.debugMode:
            return

        # デバッグ用 : もらった文字列をそのまま出力する
        print(s)


class myData:
    type = ""
    headers = []
    manager = {}
    entities = {}
    relations = {}
    comments = {}
    shapes = {}
    lines = {}
    others = {}

    def setData(self, data):

        if self.type == "[Manager]\n":
            self.manager = data

        elif self.type == "[Entity]\n":
            # PName が物理名（テーブル名）なので、それをキーとしてdictに登録する。被らないだろうし。
            self.entities[data["PName="]] = data

        elif self.type == "[Relation]\n":
            # Entity1とEntity2でリレーションを形成しているので、その2つを合成してキーに採用する。A5M2は同一場所に同一コメントの設定ができるツールなのでそれを考慮する。
            tempKey = self.getDictKey(str(data["Entity1="]) + str(data["Entity2="]), self.relations)
            self.relations[tempKey] = data

        elif self.type == "[Comment]\n":
            # コメントは同じ内容のコメントが多いので、値の全部をキーにして取り扱う。もはやキーだけでも成り立つのでは。
            tempKey = self.getDictKey(",".join(map(str, data.values())), self.comments)
            self.comments[tempKey] = data

        elif self.type == "[Shape]\n":
            # [Comment]と同様。値を全部キーにしてしまおう
            tempKey = self.getDictKey(",".join(map(str, data.values())), self.shapes)
            self.shapes[tempKey] = data

        elif self.type == "[Line]\n":
            # [Comment]と同様。値を全部キーにしてしまおう
            tempKey = self.getDictKey(",".join(map(str, data.values())), self.lines)
            self.lines[tempKey] = data

        else:
            # ここはもうなにが来るかわからんので、素直にType名と識別子でキーを作って、他を全部入れる。
            tempKey = self.getDictKey(self.type, self.others)
            self.others[tempKey] = data

    def getDictKey(self, tempKey, data):
        # もしキーが既存の場合、適当に後ろに識別子でも付ける。同じオブジェクトが存在している状況など意味不明だが、ツールとしてできてしまうので仕方ない。
        # 識別子は適当。そもそも異常な状況なので最後に一覧として出すし。識別子が被らなければ何でもよい。日時や配列数でも。
        # ちなみにA5M2のバージョン2.14 以降は項目[ZOrder]が新設されているので、それっぽいキー項目+ZOrderで必ず一意になるため、そのときにはこの関数は死蔵してよい。
        if tempKey in data:
            return tempKey + "_" + str(len(data))
        else:
            return tempKey


class myFactory:
    type = ""

    def create(self, data):

        if self.type == "[Manager]\n":
            # [Manager]部。アプリ全体的な情報。主にタブ構成とか
            return self.createManager(data)
        elif self.type == "[Entity]\n":
            # [Entity]部。いわゆるテーブル情報。
            return self.craeteEntity(data)
        elif self.type in ["[Relation]\n", "[Comment]\n", "[Shape]\n", "[Line]\n"]:
            # いまのところわかっているやつ全部。[Relation]と[Comment]と[Shape]、[Line]。
            return self.createDict(data)
        # elif self.type in ["[Line]\n"]:
        #     # 特に処理なし
        #     return data
        else:
            return data

    def createDict(self, data):
        # いまのところ[Relation]と[Comment]と[Shape]部。

        tempDict = {}

        for l in data:
            tempDict[l[:l.find("=") + 1]] = l[l.find("=") + 1:]

        return tempDict

    def craeteEntity(self, data):
        # [Entity]部。いわゆるテーブル情報。

        tempEntity = {"Field": None, "Index": None}

        tempField = {}
        tempFieldPos = 0

        tempIndex = {}
        tempIndexPos = 0

        for i, l in enumerate(data):

            if l.startswith("Field"):

                # Field を物理名をキー項目としてdictに登録。
                tempStr = l.split(",")

                # 先頭にフィールドの順番を設定
                tempField[tempStr[1]] = str(tempFieldPos) + "," + l

            elif l.startswith("IndexOption"):
                continue

            elif l.startswith("Index"):
                # 最初の「=」から次の「=」までにある物理名をキー項目としてdictに登録。Valueとしては、二個目の=の次から全部と、IndexOption全部
                tempPos = l.find("=")
                tempPos2 = l.find("=", tempPos+1)
                tempIndex[l[tempPos + 1: tempPos2]] = str(tempIndexPos) + l[tempPos2 + 1:] + "," + data[i + 1]

            else:
                tempEntity[l[:l.find("=") + 1]] = l[l.find("=") + 1:]

        # 最後にFieldとIndexを埋める
        tempEntity["Field"] = tempField
        tempEntity["Index"] = tempIndex

        return tempEntity

    def createManager(self, data):
        # [Manager]部。アプリ全体的な情報。主にタブ構成とか

        tempInfo = {"PageInfo": None}

        tempPageInfo = {}
        tempPagePos = 0

        for l in data:
            if l.startswith("PageInfo"):
                # PageInfoを、タブの名前をキー項目としてdictに登録。Value部の先頭に位置情報を付与する。dict型の選定理由は検索の容易さから。
                tempPos = l.find("\"")
                tempPos2 = l.find("\"", tempPos + 1)
                tempPageInfo[l[tempPos + 1: tempPos2]] = str(tempPagePos) + "," + l[tempPos2 + 2:]
                tempPagePos = tempPagePos + 1
            elif l.startswith("Page"):
                # 一見重要なこいつ、PageInfoさえあれば要らない子だったわ
                continue
            else:
                # 上記以外は全部ここ。「=」まででキーとする。キレイな整形もめんどいので。
                tempInfo[l[:l.find("=")+1]] = l[l.find("=")+1:]

        # 最後にPageを埋める
        tempInfo["PageInfo"] = tempPageInfo

        return tempInfo


def myIndex(value, list, pos, errorValue=-1):
    # 配列の index() って値が見つからないとValueErrorになるので、TryCatchで配列の最後を返すよ。
    try:
        return list.index(value, pos)
    except ValueError:
        return errorValue


def generateData(fileName):

    # 自分用デバッガー
    debug = myDebug()
    debug.printFree("★ファイル名 : " + fileName)

    # まずはファイル読み込み
    data0 = []
    with open(fileName, 'r', encoding='utf-8_sig') as f:    # ファイルオープン
        data0 = f.readlines()   # 各行をリストとして読み込み

    # 読み込んだのでここから全部メモリ上で処理。メモリが死んだりしたら、上の with 文の中で1行ずつ処理をするとかで工夫してください。
    eofPos = len(data0)
    debug.printFree("★行のサイズ : " + str(eofPos))

    # いろいろ初期処理
    currentPos = 0  # 読み込みするカーソル（概念）の位置
    nextSeparator = myIndex("\n", data0, currentPos)    # ブロックの終わり位置
    data = myData()  # 格納用クラスを宣言

    debug.printPositions(currentPos, nextSeparator)

    # ヘッダー部の取得
    data.headers = data0[currentPos:nextSeparator]
    debug.printData("ヘッダー", data.headers)

    # ヘッダー以降の各ブロックの処理
    factory = myFactory()   # ここからファクトリ使う。簡易ファクトリパターン

    # 配列の最後までループしますが、配列一つずつを相手にしてないので自作のmyIndexでちょっと工夫してます。
    while nextSeparator != eofPos:

        currentPos = nextSeparator + 1
        nextSeparator = myIndex("\n", data0, currentPos, eofPos)

        debug.printPositions(currentPos, nextSeparator)

        # ここで「[Manager]\n」みたいなオブジェクト判定用の文字列を与えている。
        data.type = factory.type = data0[currentPos]
        currentPos = currentPos + 1  # ブロックがわかったので、次の実データ部から読むようにカーソル（概念）を一つ進める

        data.setData(factory.create(data0[currentPos:nextSeparator]))

    return data


def diff(d0, d1):

    # https://teratail.com/questions/171217

    # header
    print(set(d0.headers) - set(d1.headers))

    a = d0.manager["PageInfo"]
    b = d1.manager["PageInfo"]

    x = a.items() - b.items()
    #x = d0.manager.items() - d1.manager.items()
    print(x)


def main(files):
    print(files)
    d0 = generateData(files[0])
    d1 = generateData(files[1])
    diff(d0, d1)
    print("main - end")


if __name__ == "__main__":

    # files = ["IYNS新お届け_ER図.a5er", "IYNS_ER図_2.a5er"]
    files = ["F:\\work\\simple_PG\\python2021\\00.a5er",
             "F:\\work\\simple_PG\\python2021\\01.a5er"]

    main(files)
