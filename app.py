from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/api/list', methods=['GET'])
def show_product():
    main = list(db.coffee.find({}, {'_id': False}))
    return jsonify({'main': main})

# @app.route('/api/info', methods=['POST'])
# def coffee_Info():
#     info_receive = request.form['name_give']
#     print(info_receive)
#     return jsonify({'msg': 'info test'})

# @app.route('/api/info', methods=['POST'])
# def show_Info():
#     info_receive = request.form['name_give']
#     print(info_receive)
#     return jsonify({'msg': 'test'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
