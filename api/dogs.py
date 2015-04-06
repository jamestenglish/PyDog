from flask.ext import restful
from db import db
from pymongo import ASCENDING, DESCENDING


class DogsList(restful.Resource):
    def get(self):
        return list(db.dogs.find({}).sort([('new_dog', DESCENDING), ('name', ASCENDING)]))