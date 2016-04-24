from flask import jsonify
from carson import app


@app.route('/api')
def placeholder():
    return jsonify({"Hello": "World"})
