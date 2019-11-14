import os

from flask import Flask, request, Response
import json
import uuid

app = Flask(__name__)

lists = {}

filename = 'data.json'


@app.teardown_appcontext
def store_data(exception):
    with open(filename, 'w') as f:
        json.dump(lists, f)


@app.before_first_request
def load_data():
    if not os.path.isfile(filename):
        return

    with open(filename, 'r') as f:
        global lists
        lists = json.load(f)


def get_base_response():
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route('/<string:name>/todo', methods=["POST", "GET", "DELETE"])
def main(name):
    resp = get_base_response()

    if name not in lists:
        lists[name] = []

    if request.method == "GET":
        resp.data = json.dumps(lists[name])

    if request.method == "POST":
        json_body = request.get_json(force=True)

        json_body['id'] = str(uuid.uuid4())

        lists[name].append(json_body)

        resp.status_code = 201
        resp.data = json.dumps(json_body)
    if request.method == "DELETE":
        todo_id = request.args.get('id')

        for todo in lists[name]:
            if todo['id'] == todo_id:
                lists[name].remove(todo)
                break

    return resp


@app.route('/lists', methods=["GET"])
def todolists():
    resp = get_base_response()

    return json.dumps(list(lists.keys()))


if __name__ == '__main__':
    app.run()
