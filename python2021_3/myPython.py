import os   # カレントディレクトリ変更で使用


class MyData:
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

    def set_data(self, data):

        if self.type == '[Manager]\n':
            self.manager = data

        elif self.type == '[Entity]\n':
            # PName が物理名（テーブル名）なので、それをキーとしてdictに登録する。被らないだろうし。
            self.entities[data['PName=']] = data

        elif self.type == '[Relation]\n':
            # Entity1とEntity2でリレーションを形成しているので、その2つを合成してキーに採用する。A5M2は同一場所に同一コメントの設定ができるツールなのでそれを考慮する。
            temp_key = self.get_dict_key(str(data['Entity1=']) + str(data['Entity2=']), self.relations)
            self.relations[temp_key] = data

        elif self.type == '[Comment]\n':
            # コメントは同じ内容のコメントが多いので、値の全部をキーにして取り扱う。もはやキーだけでも成り立つのでは。
            temp_key = self.get_dict_key(''.join(map(str, data)), self.comments)
            self.comments[temp_key] = data

        elif self.type == '[Shape]\n':
            # [Comment]と同様。値を全部キーにしてしまおう
            temp_key = self.get_dict_key(''.join(map(str, data)), self.shapes)
            self.shapes[temp_key] = data

        elif self.type == '[Line]\n':
            # [Comment]と同様。値を全部キーにしてしまおう
            temp_key = self.get_dict_key(''.join(map(str, data)), self.lines)
            self.lines[temp_key] = data

        else:
            # ここはもうなにが来るかわからんので、素直にType名と識別子でキーを作って、他を全部入れる。
            temp_key = self.get_dict_key(''.join(map(str, data)), self.others)
            self.others[temp_key] = data

    def get_dict_key(self, temp_key, data):
        # もしキーが既存の場合、適当に後ろに識別子でも付ける。同じオブジェクトが存在している状況は一部情報で意味不明だが（Relationなど）、ツールとしてできてしまうので仕方ない。
        # 識別子は適当。そもそも異常な状況なので最後に一覧として出すし。識別子が被らなければ何でもよい。日時や配列数でも。
        # ちなみにA5M2のバージョン2.14 以降は項目[ZOrder]が新設されているので、それっぽいキー項目+ZOrderで必ず一意になるため、そのときにはこの関数は死蔵してよい。
        if temp_key in data:
            return temp_key + '_' + str(len(data))
        else:
            return temp_key


class MyFactory:

    def __init__(self):
        self.type = ''

    def create(self, data):

        if self.type == '[Manager]\n':
            # [Manager]部。アプリ全体的な情報。主にタブ構成とか
            return self.create_manager(data)
        elif self.type == '[Entity]\n':
            # [Entity]部。いわゆるテーブル情報。
            return self.craete_entity(data)
        elif self.type == '[Relation]\n':
            # [Relation]部。リレーション
            return self.create_relation(data)
        elif self.type in ('[Comment]\n', '[Shape]\n', '[Line]\n'):
            # いまのところわかっているやつ全部。[Comment]と[Shape]、[Line]。
            return self.create_list(data)
        else:
            return data

    def create_list(self, data):
        temp_list = []

        for d in data:
            temp_list.append(d)

        return temp_list

    def create_relation(self, data):
        # [Relation]部。リレーション
        temp_relations = {'Entity1=': None, 'Entity2=': None, 'Data': None}

        temp_data = []

        for i, l in enumerate(data):

            if l.startswith('Entity1='):
                temp_relations['Entity1='] = l[l.find('=') + 1:]
            elif l.startswith('Entity2='):
                temp_relations['Entity2='] = l[l.find('=') + 1:]
            else:
                temp_data.append(l)

        temp_relations['Data'] = temp_data

        return temp_relations

    def craete_entity(self, data):
        # [Entity]部。いわゆるテーブル情報。

        temp_entity = {"Field": None, "Index": None, 'BaseInfo': None}

        temp_field = []
        temp_index = []
        temp_base_info = []

        for i, l in enumerate(data):

            if l.startswith('Field'):

                temp_field.append(l)

            elif l.startswith('IndexOption'):
                continue

            elif l.startswith('Index'):
                temp_index.append(l + ',' + data[i + 1])

            elif l.startswith('PName'):
                temp_entity['PName='] = l[l.find('=') + 1:]

            elif l.startswith('LName'):
                temp_entity['LName='] = l[l.find('=') + 1:]

            else:
                temp_base_info.append(l)

        # 最後にFieldとIndexを埋める
        temp_entity['Field'] = temp_field
        temp_entity['Index'] = temp_index
        temp_entity['BaseInfo'] = temp_base_info

        return temp_entity

    def create_manager(self, data):
        # [Manager]部。アプリ全体的な情報。主にタブ構成とか

        temp_info = {'PageInfo': None, 'BaseInfo': None}

        temp_page_info = []

        temp_base_info = []

        for d in data:
            if d.startswith('PageInfo'):
                temp_page_info.append(d)
            elif d.startswith('Page'):
                # 一見重要なこいつ、PageInfoさえあれば要らない子だったわ
                continue
            else:
                # 上記以外は全部ここ。「=」まででキーとする。キレイな整形もめんどいので。
                temp_base_info.append(d)

        # 最後に各情報を埋める
        temp_info['PageInfo'] = temp_page_info
        temp_info['BaseInfo'] = temp_base_info

        return temp_info


def my_index(value, list, pos, error_value=-1):
    # 配列の index() って値が見つからないとValueErrorになるので、TryCatchで配列の最後を返すよ。
    try:
        return list.index(value, pos)
    except ValueError:
        return error_value


def generate_data(file_name):

    # まずはファイル読み込み
    data0 = []
    with open(file_name, 'r', encoding='utf-8_sig') as f:    # ファイルオープン
        data0 = f.readlines()   # 各行をリストとして読み込み

    # 読み込んだのでここから全部メモリ上で処理。メモリが死んだりしたら、上の with 文の中で1行ずつ処理をするとかで工夫してください。
    eof_pos = len(data0)

    # いろいろ初期処理
    current_pos = 0  # 読み込みするカーソル（概念）の位置
    next_separator = my_index("\n", data0, current_pos)    # ブロックの終わり位置
    work_data_class = MyData()  # 格納用の一時クラスを宣言

    # ヘッダー部の取得
    work_data_class.headers = data0[current_pos:next_separator]

    # ヘッダー以降の各ブロックの処理
    factory = MyFactory()   # ここからファクトリ使う。簡易ファクトリパターン

    # 配列の最後までループしますが、配列一つずつを相手にしてないので自作のmyIndexでちょっと工夫してます。
    while next_separator != eof_pos:

        current_pos = next_separator + 1
        next_separator = my_index("\n", data0, current_pos, eof_pos)

        # ここで「[Manager]\n」みたいなオブジェクト判定用の文字列を与えている。
        work_data_class.type = factory.type = data0[current_pos]
        current_pos = current_pos + 1  # ブロックがわかったので、次の実データ部から読むようにカーソルを一つ進める

        work_data_class.set_data(factory.create(data0[current_pos:next_separator]))

    return work_data_class


def output_file(addr, data):

    with open(addr, mode='w', encoding='utf-8_sig') as f:
        # ヘッダー部
        for s in data.headers:
            f.write(s)
        f.write('\n')
        # マネージャー部
        for k, v in sorted(data.manager.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            for d in v:
                f.write(d)
        f.write('\n')
        # entity部
        for k, v in sorted(data.entities.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[Entity]\n')
            f.write('LName=' + v['LName='])
            f.write('PName=' + v['PName='])
            for d in v['Field']:
                f.write(d)
            for d in v['Index']:
                f.write(d)
            for d in v['BaseInfo']:
                f.write(d)
            f.write('\n')
        # relation
        for k, v in sorted(data.relations.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[Relation]\n')
            f.write('Entity1=' + v['Entity1='])
            f.write('Entity2=' + v['Entity2='])
            for d in v['Data']:
                f.write(d)
            f.write('\n')
        # comments
        for k, v in sorted(data.comments.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[Comment]\n')
            for d in v:
                f.write(d)
            f.write('\n')
        # shapes
        for k, v in sorted(data.shapes.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[Shape]\n')
            for d in v:
                f.write(d)
            f.write('\n')
        # lines
        for k, v in sorted(data.lines.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[Line]\n')
            for d in v:
                f.write(d)
            f.write('\n')
        # others
        for k, v in sorted(data.others.items(), key=lambda x: x[0]):    # キーでソートしながら中身を取り出す。
            f.write('[xxx]\n')
            for d in v:
                f.write(d)
            f.write('\n')


def main():
    file = 'F:\\work\\simple_PG\\python2021_3\\20211208_新お届け.a5er'

    # start_date_time = datetime.datetime.today()
    data = generate_data(file)
    output_file('F:\\work\\simple_PG\\python2021_3\\bbb.txt', data)


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルが存在するところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('- カレントディレクトリ : ' + os.getcwd())

    main()

    print('★End - PG')


# 以下、自分用メモ
