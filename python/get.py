import urllib.request
with urllib.request.urlopen("select * from yahoo.finance.xchange where https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.xchange where pair in ("USDJPY")&format=json") as res:
    html = res.read().decode("utf-8")
    print(html)
