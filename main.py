import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
		
@app.route('/add', methods=['POST'])
def add_review():
	try:
		_json = request.json
		_order_id = _json['_order_id']
		_product_id = _json['product_id']
		_user_id = _json['user_id']
		_rating	= _json['rating']
		_review = _json['review']
		_created_at = _json['created_at']
		_update_at = _json['update_at']
		# _name = _json['name']
		# _email = _json['email']
		# _password = _json['pwd']
		# validate the received values
		if _order_id and product_id and _user_id and _rating and _review and _created_at and _update_at and request.method == 'POST':
			#do not save password as a plain text
			# _hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user_review(id, order_id, product_id, use_id, rating, review, created_at, update_at) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			data = (_order_id, _product_id, _user_id, _rating, _review, _created_at, _update_at)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Review added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/reviews')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user_review")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user_review WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_order_id = _json['_order_id']
		_product_id = _json['product_id']
		_user_id = _json['user_id']
		_rating	= _json['rating']
		_review = _json['review']
		_created_at = _json['created_at']
		_update_at = _json['update_at']
		# _name = _json['name']
		# _email = _json['email']
		# _password = _json['pwd']		
		# validate the received values
		if _order_id and product_id and _user_id and _rating and _review and _created_at and _update_at and request.method == 'POST':
		# if _name and _email and _password and _id and request.method == 'POST':
		# 	#do not save password as a plain text
		# 	_hashed_password = generate_password_hash(_password)
		 	# save edits
			sql = "UPDATE tbl_user_review SET order_id=%s, product_id=%s, rating=%s, review=%s, created_at=%s, update_at=%s WHERE id=%s"
			data = (_order_id, _product_id, _user_id, _rating, _review, _created_at, _update_at)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user_review WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()