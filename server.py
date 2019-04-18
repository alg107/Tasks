from flask import Flask, jsonify, flash, request
import Tasks

app = Flask(__name__)


key = "1h8J9DHD8ZPgKU6g5uUZcOcVnkwtUUTBRDBrPkDFiv14"
credsfile = 'Goodenbour-4447ab141b22.json'

db = Tasks.Worksheet(key)
db.initialise(credsfile)

def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/tasks/')
def tasks():
    try:
        tasks = db.get_all_tasks()
        resp = jsonify([task.__dict__ for task in tasks])
        resp.status_code = 200
        return resp
    except Exception as e:
        print e

@app.route('/task/<hsh>/')
def task(hsh):
    try:
        task = db.get_task(hsh)
        if task  == 1:
            return not_found()
        else:
            return jsonify(task.__dict__)

    except Exception as e:
        print e


@app.route('/add/', methods=['POST'])
def add_user():
	try:
		_json = request.args
                
		_title = _json['title']
		_description = _json['description']
		_due = _json['due']
		# validate the received values
		if _title and _description and _due and request.method == 'POST':

                        task = Tasks.Task(_title, _description, _due)
                        new_hash = db.new_task(task)
                        
                        resp = jsonify({'message': 'User added successfully!',
                            'hash': new_hash,})
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)



@app.route('/update/<hsh>/', methods=['POST'])
def update_user(hsh):
	try:
		_json = request.args
                
		_title = _json['title']
		_description = _json['description']
		_due = _json['due']
		# validate the received values
		if _title and _description and _due and request.method == 'POST':

                        task = Tasks.Task(_title, _description, _due)
                        new_hash = db.update_task(task, hsh)
                        
                        resp = jsonify({'message': 'User updated successfully!',
                            'hash': new_hash,})
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)

@app.route('/delete/<hsh>/')
def delete_user(hsh):
	try:
                res = db.delete_task(hsh)
                if res == 1:
                    resp = jsonify("No such task found")
                else:
                    resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(500)
def page_not_found(e):
    return jsonify(error=500, text=str(e)), 500


if __name__ == "__main__":
    app.run()
