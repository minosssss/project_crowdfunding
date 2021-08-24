@temp.route('/')
def home():
    return render_template('index.html')


# # API 역할을 하는 부분
# @app.route('/login')
# def product():
#     return render_template('login.html')


# @app.route('/product')
# def product():
#     return render_template('product.html')


@temp.route('/api/list', methods=['GET'])
def show_product():
    main = list(db.coffee.find({}, {'_id': False}))
    return jsonify({'main': main})