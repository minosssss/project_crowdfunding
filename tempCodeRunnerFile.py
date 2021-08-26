@app.route('/api/product/coffee', methods=['GET'])
# def show_Info():
#     info_receive = request.args.get('product_no')
#     print(info_receive)
#     find_one = list(db.coffee.find_one(
#         {'product_no': info_receive}, {'_id': False}))
#     return jsonify({'find_one': find_one})