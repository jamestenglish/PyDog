from flask import Flask
from flask.ext import restful
from api.dogs import Dogs

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(Dogs, '/dogs/')
api.add_resource(Dogs, '/dogs/<job_id>/')


if __name__ == '__main__':
    app.run(debug=True)