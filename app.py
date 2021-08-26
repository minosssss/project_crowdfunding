from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo.collection import _FIND_AND_MODIFY_DOC_FIELDS

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/product?product_no=${product_no}')
# def product():
#     return render_template('product.html')


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


# @app.route('/api/product_info', methods=['POST', 'GET'])
# def show_Info():
#     info_receive = request.form.get('name_give', False)
#     print(info_receive)
#     find_one = list(db.coffee.find(  # DB에서 상품명에 맞는거를 찾고
#         {'title': info_receive}, {'_id': False}))
#     # [{'main_img': '//zerocoffee.net/web/product/big/202106/9f9df8442c66b14715798625f7934e02.jpg', 'title': '블렌드 제로 200g', 'price': '3,700원 ', 'info_img
#     print(find_one)
#     return jsonify({'find_one': find_one})


# @app.route('/api/product/coffee', methods=['GET'])
# def show_Info():
#     info_receive = request.args.get('product_no')
#     print(info_receive)
#     find_one = list(db.coffee.find_one(
#         {'product_no': info_receive}, {'_id': False}))
#     return jsonify({'find_one': find_one})
    # print(find_one)
    # title = find_one['title']
    # print(title)
    # return render_template('product.html', title=title)


@app.route('/api/product', methods=['GET'])
def product2():
    product_no = request.args.get('product_no')
    print(product_no)
    find_one = db.coffee.find_one({'product_no': product_no}, {'_id': False})
    title = find_one['title']
    price = find_one['price']
    main_img = find_one['main_img']
    info_img = find_one['info_img']
    return render_template('product.html', title=title, price=price, main_img=main_img, info_img=info_img)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
