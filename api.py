from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

resp = requests.get('https://localhost.com/colleges/')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for todo_item in resp.json():
    print('{} {}'.format(college_item['college_id'], college_item['summary']))


COLLEGES = {
    'college1': {'College': 'UCI'},
    'college2': {'College': 'UCSD'},
    'college3': {'College': 'UCSC'},
}


def abort_if_college_doesnt_exist(college_id):
    if college_id not in COLLEGES:
        abort(404, message="college {} doesn't exist".format(college_id))

parser = reqparse.RequestParser()
parser.add_argument('school')

class CreateUser(Resource):
    def post(self):
        return {'status': 'success'}

# College shows a single college item and lets you delete a college item
class College(Resource):
    def get(self, college_id):
        abort_if_college_doesnt_exist(college_id)
        return COLLEGES[college_id]

    def delete(self, college_id):
        abort_if_college_doesnt_exist(college_id)
        del COLLEGES[college_id]
        return '', 204

    def put(self, college_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        COLLEGES[college_id] = task
        return task, 201

class HelloWorld(Resource):
    def get(self):
        return 'Hello World. This is the home page '

# collegeList shows a list of all colleges, and lets you POST to add new colleges
class CollegeList(Resource):
    def get(self):
        return COLLEGES

    def post(self):
        args = parser.parse_args()
        college_id = int(max(COLLEGES.keys()).lstrip('college')) + 1
        college_id = 'college%i' % college_id
        COLLEGES[college_id] = {'task': args['task']}
        return COLLEGES[college_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(HelloWorld, '/')
api.add_resource(CollegeList, '/colleges')
api.add_resource(College, '/colleges/<college_id>')
api.add_resource(CreateUser, '/CreateUser')


if __name__ == '__main__':
    app.run(debug=True)