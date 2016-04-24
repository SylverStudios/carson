from flask import jsonify, request
from carson import app
from carson.github.parser import Parser


@app.route('/api')
def placeholder():
    return jsonify({"Hello": "World"})

@app.route('/accept_message/github', methods=['POST'])
def accept_github_message():
    parsed = Parser().parse_comment_message(request.get_json(force=True))
    print(parsed)
    return jsonify(parsed)
