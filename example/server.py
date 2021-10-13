from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        return render_template('home.html', title='Home', course='EDD', login=True)
    return render_template('home.html', title='Home', course='EDD')



@app.route('/login', methods=['POST'])
# @cross_origin()
def login():
    content = request.get_json()
    print(content)
    return {'login': True}



@app.route('/test')
@app.route('/test/<name>')
def test(name=None):
    if request.args:
        print(request.args)
    if name:
        return name
    return 'Hola'