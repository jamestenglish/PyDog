from rq.decorators import job
from redis import q
from db import db
import sys

@job(queue=q)
def scrape(job_id):
    try:
        pass
    except:  # if ANYTHING goes wrong with the job we want to update the job db
        error_str = sys.exc_info()[0]
        update = {'$set': {
            'done': True,
            'percent': 100,
            'error': error_str
        }}
        db.find_one_and_update({'job_id', job_id}, update)
    pass