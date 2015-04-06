from flask.ext import restful
from db import db


class DogsList(restful.Resource):
    def get(self):
        return list(db.dogs.find({}).sort('name'))