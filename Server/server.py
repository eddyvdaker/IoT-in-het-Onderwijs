"""
StudyBuddy Server
"""

from flask import abort, Flask, jsonify, request

from database import *
from queries import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    pass


"""
Retrieving Data API Calls
"""


# Get a list of study events for a certain student ID
# Used as 'GET /events?id=<studentID>'
@app.route('/events', methods=['GET'])
def get_study_events():
    student_id = request.args.get('id')
    query = get_study_events_query(student_id)
    data = execute_read_query(db, query)
    cleaned_data = []
    for row in data:
        cleaned_data.append(list(row)[0])
    return jsonify({'events': cleaned_data})


# Get details of a specific study event, contains a list of sessions
# Used as 'GET /event?id=<eventID>'
@app.route('/event', methods=['GET'])
def get_study_event():
    event_id = request.args.get('id')
    query = get_study_event_query(event_id)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    cleaned_data = {}
    for i, col in enumerate(data):
        cleaned_data.update({columns[i]: col})
    return jsonify(cleaned_data)


# Get a list of all study sessions linked to a study event
# Used as 'GET /sessions?id=<eventID>'
@app.route('/sessions', methods=['GET'])
def get_study_sessions():
    event_id = request.args.get('id')
    query = get_study_sessions_query(event_id)
    data = execute_read_query(db, query)
    cleaned_data = []
    for row in data:
        cleaned_data.append(list(row)[0])
    return jsonify({'sessions': cleaned_data})


# Get details of a session, includes the data generated for that session
# Used as 'GET /session?id=<sessionID>'
@app.route('/session', methods=['GET'])
def get_study_session():
    session_id = request.args.get('id')
    query = get_study_session_query(session_id)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'activityid', 'start_time', 'stop_time', 'session_date']
    cleaned_data = {}
    for i, col in enumerate(data):
        cleaned_data.update({columns[i]: col})
    print(cleaned_data)
    return jsonify(cleaned_data)


# Get a list of data objects belonging to a study session:
# Used as 'GET /data_list?id=<sessionID>'
# Optionally include a type:
# Used as: 'GET /data_list?id=<sessionID>&type=<data_type?>'
@app.route('/data_list', methods=['GET'])
def get_data_list():
    session_id = request.args.get('id')
    query = get_data_list_query(session_id)
    data = execute_read_query(db, query)
    cleaned_data = []
    for row in data:
        cleaned_data.append(list(row)[0])
    print(cleaned_data)
    return jsonify({'data list': cleaned_data})


# Get data from a data object
# Used as 'GET /data?id=<dataID>'
@app.route('/data', methods=['GET'])
def get_data():
    data_id = request.args.get('id')
    query = get_data_query(data_id)
    data = list(execute_read_query(db, query)[0])
    print(data)
    columns = ['id', 'sessionid', 'sessiondata', 'data_type']
    cleaned_data = {}
    for i, col in enumerate(list(data)):
        cleaned_data.update({columns[i]: col})
    print(cleaned_data)
    return jsonify(cleaned_data)


"""
Session API Calls
"""


# Toggle (start/top) session for a set eventID
# Used as 'GET /toggle_session?id=<eventID>'
@app.route('/toggle_session', methods=['GET'])
def toggle_session():
    pass


# Check if a session has been started for a studentID
# Used as 'GET /check_session?id=<studentID>'
@app.route('/check_session', methods=['GET'])
def check_session():
    pass


"""
Posting New Data API Calls
"""


# Create a new study event
# Used as 'POST /event {studentID, moduleID, teacherID, title, description,
# category, notes, status}'
@app.route('/event', methods=['POST'])
def new_study_event():
    if not request.json:
        abort(400)
    event_details = request.json



"""
Testing Calls
"""


# Test if the receiving post request with json objects is working
# Used as 'POST /testing_post JSON_OBJECT'
@app.route('/testing_post', methods=['POST'])
def test_post():
    if not request.json:
        abort(400)
    post = request.json
    print(f'testing post: {post}')
    return jsonify(post)


# Test if get requests are working with passing variables
# Used as 'GET /testing_get?var=<test_variable>'
@app.route('/testing_get', methods=['GET'])
def test_get():
    var = request.args.get('var')
    print(f'testing get: {var}')
    return var


"""
Start Server
"""

if __name__ == '__main__':
    print('Starting StudyBuddy Server...')

    print('Initializing database...')
    i = 0
    while not check_db():
        i += 1
        print('Database not found, creating new database...')
        create_db()
        if i >= 5:
            print('Error: cannot create database!')
            exit()
    db = initialize_db()
    print('Database initialized...')

    print('Starting Flask application...')
    app.run(host='0.0.0.0')
