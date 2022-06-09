# AWSCloudHSM を windows で使う方法

以下の手順を実施する。

1. AWS CloudHSM client のインストール
2. JCE provider のインストール

## 1. AWSCloudHSM クライアントインストール

公式サイトからインストーラーをダウンロードし、それをインストールする。

### 1. 以下からインストーラーを取得

- [AWS公式サイト（英語）](https://docs.aws.amazon.com/cloudhsm/latest/userguide/install-and-configure-client-win.html)

- [ダウンロードリンク（直リンク）](https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/Windows/AWSCloudHSMClient-latest.msi)

### 2. 管理者権限でインストーラーを起動

- *.msi は 管理者権限での実行ができないので、コマンドプロンプト経由で行う。

1. コマンドプロンプトを管理者権限で起動する。

2. インストーラーが存在するディレクトリに移動する。

3. 以下のコマンドを実行する。

```cmd
msiexec /i AWSCloudHSMClient-latest.msi
```

### 3. 実行後確認

以下ディレクトリが作成されていること。

1. C:\Program Files\Amazon\CloudHSM
2. C:\ProgramData\Amazon\CloudHSM

## 2. JCE provider のインストール

JCE provider をインストールする必要があるが、Windowsにはインストーラーがない。  

- [公式サイト](https://docs.aws.amazon.com/cloudhsm/latest/userguide/java-library-install.html)

公式サイトには rpm が置いてあるので、いったんダウンロードしてから windows 上で展開する。

- [rpm の アドレス](https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL7/cloudhsm-client-jce-latest.el7.x86_64.rpm)

rpm は windows 標準搭載の 7zip で開けば中身が見れるし展開できるので、フツーに取り出す。

## 3. Windows 環境に、ライブラリを認識させる。

あああ

## 99. 他

- https://www.fixes.pub/program/805579.html
- https://docsplayer.net/82960151-Aws-cloudhsm-%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%AC%E3%82%A4%E3%83%89.html
