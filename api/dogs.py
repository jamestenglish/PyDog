from flask.ext import restful


class Dogs(restful.Resource):
    def get(self):
        return {'hello': 'world'}