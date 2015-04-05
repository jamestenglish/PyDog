from flask import Flask, render_template
from flask.ext import restful
from api.dogs import DogsList
from api.jobs import DogScrape


app = Flask(__name__)
api = restful.Api(app)

api.add_resource(DogsList, '/dogs/')
api.add_resource(DogScrape, '/jobs/dogscrape/<job_id>/')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)