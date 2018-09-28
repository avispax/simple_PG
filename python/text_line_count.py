# ファイルをオープンする
import glob
# テキストファイルのみを取得
files = glob.glob("C:\\\\work\\task\\source\\01_ATMGW\\webapps\\trunk\\WebContent\\WEB-INF\\conf\\individual\\*.xml")
for file in files:
  num_lines = sum(1 for line in open(file, "r", encoding="utf-8_sig"))
  print(file + "-" + str(num_lines))
