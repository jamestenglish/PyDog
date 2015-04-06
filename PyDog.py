from flask import Flask, render_template, make_response
from flask.ext import restful
from api.dogs import DogsList
from api.job_runner import DogScrape
from db import db
import json
import uuid
from datetime import datetime
from bson.objectid import ObjectId


app = Flask(__name__)
api = restful.Api(app)

api.add_resource(DogsList, '/dogs/')
api.add_resource(DogScrape, )
api.add_resource(DogScrape, '/jobs/dog_scrape/<job_id>/',
                            '/jobs/dog_scrape/')


@app.route('/')
def index():
    return render_template('index.html')


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)

        if isinstance(obj, uuid.UUID):
            return '{}'.format(obj)

        if isinstance(obj, ObjectId):
            return '{}'.format(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, cls=ComplexEncoder), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    db.settings.update({'id': 1},
                       {'$set': {'zip_code': 67218,
                                 'breed_filter': ''}},
                       upsert=True)
    app.run(debug=True)


