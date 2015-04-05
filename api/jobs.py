from flask.ext import restful
from db import db
from uuid import uuid4
from jobs.scrape import scrape


class DogScrape(restful.Resource):
    def post(self):
        job_id = uuid4()
        job = {'type': 'DogScrape',
               'done': False,
               'percent': 0,
               'job_id': job_id,
               'error': ''}
        db.jobs.insert_one(job)

        scrape.delay(job_id)

        return {'job_id': job_id}

    def get(self, job_id):
        return db.find_one({'job_id', job_id})