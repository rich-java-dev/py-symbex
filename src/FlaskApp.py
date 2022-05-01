'''

Flask App to convert CLI program into Reactive Web Server.

author: Richard White

'''
from flask_cors import CORS
from flask import Flask, request
from symbex import ModuleParser


app = Flask(__name__)
CORS(app)


@app.route('/run', methods=['POST'])
def run():
    print("RUN CALLED...")

    payload: str = request.data

    print(payload)
    parser: ModuleParser = ModuleParser(payload)

    parser.parse()
    parser.results()

    resp: dict = {
        'ast': parser.get_ast(),
        'results': parser.results()
    }
    return resp


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
