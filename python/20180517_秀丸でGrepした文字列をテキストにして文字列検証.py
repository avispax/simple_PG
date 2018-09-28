# ファイルをオープンする
fff = open("C:\\work\\aaa.txt", "r")


f = open("bbb.txt", "w", encoding="shift_jis")
f.write('■スタート')

# 一行ずつ読み込んでは表示する
for lxx in fff:
  if ('* @' in lxx) or ('@SuppressWarnings' in lxx) or ('@Override' in lxx) or ('@Test' in lxx):
    pass
  else:
    f.write(lxx)
    print(lxx)

# ファイルをクローズする
f.close
fff.close()
