from flask.ext import restful
from db import db


class Dogs(restful.Resource):
    def get(self):
        return list(db.dogs.find_all())