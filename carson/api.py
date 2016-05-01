from flask import jsonify, request
from carson import app
from carson.github.parser import Parser


@app.route('/api')
def placeholder():
    return jsonify({"Hello": "World"})

# Pull Requests are considered Issues in this part of the API
@app.route('/messages/github/issue_comment', methods=['POST'])
def handle_github_issue_comment():
    parsed = Parser().parse_comment_message(request.get_json(force=True))
    print(parsed)
    return jsonify(parsed)

# Services reports
@app.route('/messages/github/commit_status', methods=['POST'])
def handle_github_commit_status():
    parsed = Parser().parse_commit_status(request.get_json(force=True));
    print(parsed)
    return jsonify(parsed)
