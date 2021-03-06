from flask.ext import restful
from db import db
from uuid import uuid4, UUID
from jobs.scrape import scrape
from datetime import datetime, timedelta
from pymongo import DESCENDING


class DogScrape(restful.Resource):
    def post(self):

        jobs_cursor = db.jobs.find({}).sort('date', DESCENDING)

        if jobs_cursor.count() > 0:
            latest_job = jobs_cursor[0]
            latest_date = latest_job['date']
            now = datetime.now()
            delta = now - latest_date

            thirty_delta = timedelta(minutes=30)
            if thirty_delta > delta and len(latest_job['error']) == 0:
                return {'error': 'Please wait {} '.format(thirty_delta-delta)}

        job_id = uuid4()
        job = {'type': 'DogScrape',
               'done': False,
               'percent': 0,
               'job_id': job_id,
               'error': '',
               'date': datetime.now()}
        db.jobs.insert(job)

        scrape.delay(job_id)

        return {'job_id': job_id}

    def get(self, job_id):
        return db.jobs.find({'job_id': UUID(job_id)})[0]