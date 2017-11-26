from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

COLLEGES = {
    'school1': {'school_name': 'UCLA'},
    'school2': {'school_name': 'UCI'},
    'school3': {'school_name': 'UCR'},
}

def abort_if_college_doesnt_exist(college_id):
    if college_id not in COLLEGES:
        abort(404, message="college {} doesn't exist".format(college_id))

parser = reqparse.RequestParser()
parser.add_argument('school_name')

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
        print(args)
        school_name = {'school_name': args['school_name']}
        COLLEGES[college_id] = school_name
        return school_name, 201


# TodoList
# shows a list of all COLLEGES, and lets you POST to add new school_names
class CollegeList(Resource):
    def get(self):
        # Returns JSON object of Colleges, including school_name and the value
        return COLLEGES

    def post(self):
        args = parser.parse_args()
        college_id = int(max(COLLEGES.keys()).lstrip('school')) + 1
        college_id = 'school%i' % college_id
        COLLEGES[college_id] = {'school_name': args['school_name']}
        return COLLEGES[college_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(CollegeList, '/colleges')
api.add_resource(College, '/colleges/<college_id>')


if __name__ == '__main__':
    app.run(debug=True)