from flask import Flask
import odd

app = Flask(__name__)

@app.route('/')
def hello() -> str:
  return 'Hello world from Flask!'

@app.route('/test')
def h2() -> str:
  word = "---------------- test hello world my test. -------------------"
  return word

app.run()
