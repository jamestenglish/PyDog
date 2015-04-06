from flask.ext import restful
from db import db
from uuid import uuid4, UUID
from jobs.scrape import scrape
from datetime import datetime
from pymongo import ASCENDING, DESCENDING


class DogScrape(restful.Resource):
    def post(self):

        jobs_cursor = db.jobs.find({}).sort('date', DESCENDING)

        if jobs_cursor.count() > 0:
            latest_job = jobs_cursor[0]
            latest_date = latest_job['date']
            now = datetime.now()
            delta = now - latest_date

            minutes = (delta.seconds % 3600) // 60
            if minutes < 30 and len(latest_job['error']) == 0:
                return {'error': 'Please wait {} minutes. Last Run: {}'.format(30 - minutes, latest_date)}

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