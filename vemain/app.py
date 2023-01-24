from flask import Flask,render_template
from flask import request
from deep_translator import GoogleTranslator
app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"])
def Doget():
    if request.method == 'POST':
        text = request.form['text'] # formのname = "text"を取得
        translated = GoogleTranslator(source='auto',target='en').translate(text)
        return render_template('test.html', text = translated)
        
    else:
        return render_template('test.html')



