from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        print(request.form.get('slocation'))
        path = [
                {'lat':42.37807,'lng':-72.51993},
                {'lat':42.37864,'lng':-72.51993},
                {'lat':42.37958,'lng':-72.51959}
                ]
        pathJson = json.dumps(path,ensure_ascii=False)
        print(pathJson)
        return render_template('index.html',path=pathJson,isPath="true")
    return render_template('index.html', isPath="false")

