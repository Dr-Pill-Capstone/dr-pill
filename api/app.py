from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

CREATORS = ["Sheshank", "Shubh", "Kriya", "Richard"]

class TestClass(Resource):
    # Testing methods for api
    def __init__(self) -> None:
        self.creators = CREATORS
        super().__init__()

    @app.route("/")
    def test_entry():
        return "Hello Dr. Pill!"
    
    @app.route("/creators", methods=['GET'])
    def test_creators(self):
        print(f"My creators are: {creator}" for creator in self.creators)
        return 
    
test = TestClass()
api.add_resource(test, '/test') # /test is the entry point to test basic API functionality

@app.route("/home/")
def test_hello():
    return "Hello!"

if __name__ == '__main__':
    app.run()

