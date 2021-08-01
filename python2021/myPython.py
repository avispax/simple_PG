import difflib
import datetime


class myDebug:
    def __init__(self):
        self.debugMode = False

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

    def __init__(self):
        self.type = ""
        self.headers = []
        self.manager = {}
        self.entities = {}
        self.relations = {}
        self.comments = {}
        self.shapes = {}
        self.lines = {}
        self.others = {}

    def setData(self, data):

        if self.type == '[Manager]\n':
            self.manager = data

        elif self.type == '[Entity]\n':
            # PName が物理名（テーブル名）なので、それをキーとしてdictに登録する。被らないだろうし。
            self.entities[data['PName=']] = data

        elif self.type == '[Relation]\n':
            # Entity1とEntity2でリレーションを形成しているので、その2つを合成してキーに採用する。A5M2は同一場所に同一コメントの設定ができるツールなのでそれを考慮する。
            tempKey = self.getDictKey(str(data['Entity1=']) + str(data['Entity2=']), self.relations)
            self.relations[tempKey] = data

        elif self.type == '[Comment]\n':
            # コメントは同じ内容のコメントが多いので、値の全部をキーにして取り扱う。もはやキーだけでも成り立つのでは。
            tempKey = self.getDictKey(''.join(map(str, data)), self.comments)
            self.comments[tempKey] = data

        elif self.type == '[Shape]\n':
            # [Comment]と同様。値を全部キーにしてしまおう
            tempKey = self.getDictKey(''.join(map(str, data)), self.shapes)
            self.shapes[tempKey] = data

        elif self.type == '[Line]\n':
            # [Comment]と同様。値を全部キーにしてしまおう
            tempKey = self.getDictKey(''.join(map(str, data)), self.lines)
            self.lines[tempKey] = data

        else:
            # ここはもうなにが来るかわからんので、素直にType名と識別子でキーを作って、他を全部入れる。
            tempKey = self.getDictKey(''.join(map(str, data)), self.others)
            self.others[tempKey] = data

    def getDictKey(self, tempKey, data):
        # もしキーが既存の場合、適当に後ろに識別子でも付ける。同じオブジェクトが存在している状況は一部情報で意味不明だが（Relationなど）、ツールとしてできてしまうので仕方ない。
        # 識別子は適当。そもそも異常な状況なので最後に一覧として出すし。識別子が被らなければ何でもよい。日時や配列数でも。
        # ちなみにA5M2のバージョン2.14 以降は項目[ZOrder]が新設されているので、それっぽいキー項目+ZOrderで必ず一意になるため、そのときにはこの関数は死蔵してよい。
        if tempKey in data:
            return tempKey + '_' + str(len(data))
        else:
            return tempKey


class myFactory:

    def __init__(self):
        self.type = ''

    def create(self, data):

        if self.type == '[Manager]\n':
            # [Manager]部。アプリ全体的な情報。主にタブ構成とか
            return self.createManager(data)
        elif self.type == '[Entity]\n':
            # [Entity]部。いわゆるテーブル情報。
            return self.craeteEntity(data)
        elif self.type == '[Relation]\n':
            # [Relation]部。リレーション
            return self.createRelation(data)
        elif self.type in ('[Comment]\n', '[Shape]\n', '[Line]\n'):
            # いまのところわかっているやつ全部。[Comment]と[Shape]、[Line]。
            return self.createList(data)
        else:
            return data

    def createList(self, data):
        tempList = []

        for l in data:
            tempList.append(l)

        return tempList

    def createRelation(self, data):
        # [Relation]部。リレーション
        tempRelations = {'Entity1=': None, 'Entity2=': None, 'Data': None}

        tempData = []

        for i, l in enumerate(data):

            if l.startswith('Entity1='):
                tempRelations['Entity1='] = l[l.find('=') + 1:]
            elif l.startswith('Entity2='):
                tempRelations['Entity2='] = l[l.find('=') + 1:]
            else:
                tempData.append(l)

        tempRelations['Data'] = tempData

        return tempRelations

    def craeteEntity(self, data):
        # [Entity]部。いわゆるテーブル情報。

        tempEntity = {"Field": None, "Index": None, 'BaseInfo': None}

        tempField = []
        tempIndex = []
        tempBaseInfo = []

        for i, l in enumerate(data):

            if l.startswith('Field'):

                tempField.append(l)

            elif l.startswith('IndexOption'):
                continue

            elif l.startswith('Index'):
                tempIndex.append(l + ',' + data[i + 1])

            elif l.startswith('PName'):
                tempEntity['PName='] = l[l.find('=') + 1:]
            else:
                tempBaseInfo.append(l)

        # 最後にFieldとIndexを埋める
        tempEntity['Field'] = tempField
        tempEntity['Index'] = tempIndex
        tempEntity['BaseInfo'] = tempBaseInfo

        return tempEntity

    def createManager(self, data):
        # [Manager]部。アプリ全体的な情報。主にタブ構成とか

        tempInfo = {'PageInfo': None, 'BaseInfo': None}

        tempPageInfo = []

        tempBaseInfo = []

        for l in data:
            if l.startswith('PageInfo'):
                tempPageInfo.append(l)
            elif l.startswith('Page'):
                # 一見重要なこいつ、PageInfoさえあれば要らない子だったわ
                continue
            else:
                # 上記以外は全部ここ。「=」まででキーとする。キレイな整形もめんどいので。
                tempBaseInfo.append(l)

        # 最後に各情報を埋める
        tempInfo['PageInfo'] = tempPageInfo
        tempInfo['BaseInfo'] = tempBaseInfo

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
    myDataClass = myData()  # 格納用クラスを宣言

    debug.printPositions(currentPos, nextSeparator)

    # ヘッダー部の取得
    myDataClass.headers = data0[currentPos:nextSeparator]
    debug.printData("ヘッダー", myDataClass.headers)

    # ヘッダー以降の各ブロックの処理
    factory = myFactory()   # ここからファクトリ使う。簡易ファクトリパターン

    # 配列の最後までループしますが、配列一つずつを相手にしてないので自作のmyIndexでちょっと工夫してます。
    while nextSeparator != eofPos:

        currentPos = nextSeparator + 1
        nextSeparator = myIndex("\n", data0, currentPos, eofPos)

        debug.printPositions(currentPos, nextSeparator)

        # ここで「[Manager]\n」みたいなオブジェクト判定用の文字列を与えている。
        myDataClass.type = factory.type = data0[currentPos]
        currentPos = currentPos + 1  # ブロックがわかったので、次の実データ部から読むようにカーソル（概念）を一つ進める

        myDataClass.setData(factory.create(data0[currentPos:nextSeparator]))

    return myDataClass


def diffLib(l0, l1):
    matcher = difflib.SequenceMatcher(None, l0, l1)

    tempResults = []

    # 比較しつつ、ついでにある程度データを読めるように。整形ってほどではない。
    for tag, i0, i1, j0, j1 in matcher.get_opcodes():
        if tag == 'replace':
            tempResults.append([tag, l0[i0], l1[j0]])
        elif tag == 'insert':
            tempResults.append([tag, ' ', l1[j0]])
        elif tag == 'delete':
            tempResults.append([tag, l0[i0], ' '])

    return tempResults


def myDiff(d0, d1):

    # Header
    results = {'header': diffLib(d0.headers, d1.headers)}

    # Manager
    results['ManagerBase'] = diffLib(d0.manager['BaseInfo'], d1.manager['BaseInfo'])

    # Manager2 : タブ情報部分
    results['ManagerPageInfo'] = diffLib(d0.manager['PageInfo'], d1.manager['PageInfo'])

    # Entity : テーブル情報そもそもの有無を keys を利用して判定
    results['EntityKeys'] = diffLib(list(d0.entities.keys()), list(d1.entities.keys()))

    # Entity2 : とりあえず両方に同じテーブル名があるやつを対象に、中身の一致確認
    results['Entities'] = None
    tempEntities = {}
    for e in d0.entities:
        if e in d1.entities:
            # ここにきたら両データに存在するってことなので、比較処理まで可能。
            tempEnt = {'EntityBase': None, 'Fields': None, 'Index': None}
            tempEnt['EntityBase'] = diffLib(d0.entities[e]['BaseInfo'], d1.entities[e]['BaseInfo'])
            tempEnt['Fields'] = diffLib(d0.entities[e]['Field'], d1.entities[e]['Field'])
            tempEnt['Index'] = diffLib(d0.entities[e]['Index'], d1.entities[e]['Index'])
            # 上記3項目が全部空っぽ（差分なし）なら格納しなくていいや
            if not len(tempEnt['EntityBase']) == len(tempEnt['Fields']) == len(tempEnt['Index']) == 0:
                tempEntities[e] = tempEnt

    results['Entities'] = tempEntities

    # Relation1 : リレーがそもそも増えたり減ったりを判定。内容の一致確認はその2で。
    results['RelationKeys'] = diffLib(list(d0.relations.keys()), list(d1.relations.keys()))

    # Relation2 : キーはあるけど内容が一致してるかどうか
    tempRelation = {}
    for e in d0.relations:
        if e in d1.relations:
            tempRel = {'Data': diffLib(d0.relations[e]['Data'], d1.relations[e]['Data'])}
            if not len(tempRel['Data']) == 0:
                tempRelation[e] = tempRel

    results['Relations'] = tempRelation

    # Comment1 : keys
    results['CommentKeys'] = diffLib(list(d0.comments.keys()), list(d1.comments.keys()))

    # Comment2 : 内容
    tempComment = {}
    for e in d0.comments:
        if e in d1.comments:
            tempCom = {'Data': diffLib(d0.comments[e], d1.comments[e])}
            if not len(tempCom['Data']) == 0:
                tempComment[e] = tempCom

    results['Comments'] = tempComment

    # Shape1 : keys
    results['ShapeKeys'] = diffLib(list(d0.shapes.keys()), list(d1.shapes.keys()))

    # Shape2 : 内容
    tempShape = {}
    for e in d0.shapes:
        if e in d1.shapes:
            tempSh = {'Data': diffLib(d0.shapes[e], d1.shapes[e])}
            if not len(tempSh['Data']) == 0:
                tempShape[e] = tempSh

    results['Shapes'] = tempShape

    # Line1 : keys
    results['LineKeys'] = diffLib(list(d0.lines.keys()), list(d1.lines.keys()))

    # Line2 : 内容
    tempLine = {}
    for e in d0.lines:
        if e in d1.lines:
            tempLn = {'Data': diffLib(d0.lines[e], d1.lines[e])}
            if not len(tempLn['Data']) == 0:
                tempLine[e] = tempLn

    results['Lines'] = tempLine

    # Other1 : keys
    results['OtherKeys'] = diffLib(list(d0.others.keys()), list(d1.others.keys()))

    # Other2 : 内容
    tempOther = {}
    for e in d0.others:
        if e in d1.others:
            tempOth = {'Data': diffLib(d0.others[e], d1.others[e])}
            if not len(tempOth['Data']) == 0:
                tempOther[e] = tempOth

    results['Others'] = tempOther

    return results


def generateMarkdown(files, diffData, startDateTime):

    outputFileName = 'myDiff_' + startDateTime.strftime("%Y%m%d%H%M%S") + '.md'

    # ファイルサマリを生成する。
    md = ['# diff : ' + files[0] + ' - ' + files[1] + ' : ' + startDateTime.strftime("%Y/%m/%d %H:%M:%S")]
    md.append('\n')
    md.append('- ファイルその1 : ' + files[0])
    md.append('- ファイルその2 : ' + files[1])
    md.append('- 比較日時 : ' + startDateTime.strftime("%Y/%m/%d %H:%M:%S"))
    md.append('- Markdownファイル名 : ' + outputFileName)
    md.append('\n')

    # header 情報を生成する
    md.append('## ヘッダー部')
    md.append('\n')
    genMd(md, diffData['header'])

    # Manager1を生成する
    md.append('## Manager1 : Base')
    md.append('\n')
    genMd(md, diffData['ManagerBase'])

    # Manager2を生成する
    md.append('## Manager2 : PageInfo')
    md.append('\n')
    genMd(md, diffData['ManagerPageInfo'])

    # Entity1を生成する
    md.append('## Entity1 : Keys')
    md.append('\n')
    genMd(md, diffData['EntityKeys'])

    # Entity2を生成する
    md.append('## Entity2 : Entities')
    md.append('\n')
    for e in diffData['Entities']:
        md.append('### Entity : ' + e)
        md.append('\n')

        # EntityBase
        md.append('#### EntityBase')
        md.append('\n')
        genMd(md, diffData['Entities'][e]['EntityBase'])

        # EntityFields
        md.append('#### Fields')
        md.append('\n')
        genMd(md, diffData['Entities'][e]['Fields'])

        # EntityFields
        md.append('#### Index')
        md.append('\n')
        genMd(md, diffData['Entities'][e]['Index'])

    # Relation1を生成する
    md.append('## Relation1 : Keys')
    md.append('\n')
    genMd(md, diffData['RelationKeys'])

    # Relation2を生成する
    md.append('## Relation2 : Relations')
    md.append('\n')
    for e in diffData['Relations']:
        md.append('### Relation : ' + e)
        md.append('\n')

        # Data
        md.append('#### Data')
        md.append('\n')
        genMd(md, diffData['Relations'][e]['Data'])

    # Comment1を生成する
    md.append('## Comment1 : Keys')
    md.append('\n')
    genMd(md, diffData['CommentKeys'])

    # Comment2を生成する
    md.append('## Comment2 : Comments')
    md.append('\n')
    for e in diffData['Comments']:
        md.append('### Comment : ' + e)
        md.append('\n')

        # Data
        md.append('#### Data')
        md.append('\n')
        genMd(md, diffData['Comments'][e]['Data'])

    # Shape1を生成する
    md.append('## Shape1 : Keys')
    md.append('\n')
    genMd(md, diffData['ShapeKeys'])

    # Shape2を生成する
    md.append('## Shape2 : Shapes')
    md.append('\n')
    for e in diffData['Shapes']:
        md.append('### Shapes : ' + e)
        md.append('\n')

        # Data
        md.append('#### Data')
        md.append('\n')
        genMd(md, diffData['Comments'][e]['Data'])

    # Line1を生成する
    md.append('## Line1 : Keys')
    md.append('\n')
    genMd(md, diffData['LineKeys'])

    # Lines2を生成する
    md.append('## Line2 : Lines')
    md.append('\n')
    for e in diffData['Lines']:
        md.append('### Lines : ' + e)
        md.append('\n')

        # Data
        md.append('#### Data')
        md.append('\n')
        genMd(md, diffData['Lines'][e]['Data'])

    # Other1を生成する
    md.append('## Other1 : Keys')
    md.append('\n')
    genMd(md, diffData['OtherKeys'])

    # Other2を生成する
    md.append('## Other2 : Others')
    md.append('\n')
    for e in diffData['Others']:
        md.append('### Others : ' + e)
        md.append('\n')

        # Data
        md.append('#### Data')
        md.append('\n')
        genMd(md, diffData['Others'][e]['Data'])

    return md


def genMd(md, data):

    if len(data) > 0:

        md.append('- 相違件数 : ' + str(len(data)) + ' 件')
        md.append('\n')
        md.append('| No. | 区分 | 比較 A | 比較 B |')
        md.append('|:--:|:--|:--|:--|')

        for i, d in enumerate(data):
            if d[0] in ['replace', 'insert', 'delete']:
                md.append('|' + str(i) + '|' + '|'.join(d).replace('\n', '<BR>') + '|')

    else:
        md.append('- 差異なし')

    md.append('\n')


def outputFile(outputAddr, md):

    with open(outputAddr, mode='w', encoding='utf-8_sig') as f:
        for s in md:
            f.write(s + '\n')


def main(files):
    startDateTime = datetime.datetime.today()
    d0 = generateData(files[0])
    d1 = generateData(files[1])
    diffSummary = myDiff(d0, d1)
    md = generateMarkdown(files, diffSummary, startDateTime)
    outputFileAddr = 'F:\\work\\simple_PG\\python2021\\myDiff_' + startDateTime.strftime("%Y%m%d%H%M%S") + '.md'
    outputFile(outputFileAddr, md)

    print('main - end')


if __name__ == '__main__':

    # files = ["IYNS新お届け_ER図.a5er", "IYNS_ER図_2.a5er"]
    files = ['F:\\work\\simple_PG\\python2021\\00.a5er',
             'F:\\work\\simple_PG\\python2021\\01.a5er']

    main(files)
