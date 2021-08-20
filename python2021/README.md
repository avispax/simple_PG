# A5M2 を 2 つ読み込んで一つにマージしたりしよう。

## いまのところの対象の部品

- '[Relation]\n', '[Entity]\n', '[Manager]\n', '[Line]\n', '[Comment]\n', '[Shape]\n'

## diffLib

Python のライブラリの「diffLib」に List 型で渡すと Diff が楽っぽいので、dict 型と list 型を混ぜて使う。  
差分比較をする末端では List。その List を格納するところは dict としている感じ。たしか。

## リファクタリング

なにもしてない。誰かかっこよくやってくれ。

## マージについて

単純な insert ぐらいならやってもいいかもしれないけど、delete や replace はこれを使うプロジェクトにおいて微妙なんだよね。  
というわけで、いったん insert もなしで、差をそのまま利用者（自分）に還元する。

## アウトプットについて

Markdown でやる。

まぁこんな感じ ↓

## header

- 相違件数 : n

| No. | 区分    | 比較 A | 比較 B |
| :-: | :------ | :----- | :----- |
|  1  | replace | aaa    | bbb    |
|  2  | insert  |        | bbb    |
|  3  | delete  | aaa    |        |

もしくは

- なし
