"""
StudyBuddy Server
"""

from flask import abort, Flask, jsonify, redirect, render_template, request
from os import remove
from urllib.request import urlopen
import subprocess

from dashboard import *
from database import *
from queries import *

app = Flask(__name__)


@app.route('/user/<username>', methods=['GET'])
def student_page(username):
    query = get_study_events_query(username)
    data = execute_read_query(db, query)
    cleaned_data = []
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    for row in data:
        new_row = {}
        for y, col in enumerate(list(row)):
            new_row.update({columns[y]: col})
        cleaned_data.append(new_row)
    page_vars = {'events': cleaned_data}
    page_vars.update({'username': username})

    return render_template('overview.html', page_vars=page_vars)


@app.route('/activity/<activity>', methods=['GET'])
def activity_page(activity):
    query = get_study_event_query(activity)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    page_vars = {}
    for i, col in enumerate(data):
        page_vars.update({columns[i]: col})

    page_vars.update({'username': page_vars['studentid']})
    return render_template('activity.html', page_vars=page_vars)


# Returns the not logged in homepage, in this PoC it only contains
# a field for selecting a user, in the real version of this system
# it will be a login screen.
@app.route('/', methods=['GET'])
def homepage():
    return render_template('base.html', page_vars='')


"""
Retrieving Data API Calls
"""


# Get a list of study events for a certain student ID
# Used as 'GET /events_list?id=<studentID>'
@app.route('/events_list', methods=['GET'])
def get_study_events_list():
    student_id = request.args.get('id')
    query = get_study_events_list_query(student_id)
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


# Get details of all study events of an student ID
# Used as 'GET /events?id=<studentID>'
@app.route('/events', methods=['GET'])
def get_study_events():
    student_id = request.args.get('id')
    query = get_study_events_query(student_id)
    data =execute_read_query(db, query)
    cleaned_data = []
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    for row in data:
        new_row = {}
        for y, col in enumerate(list(row)):
            new_row.update({columns[y]: col})
        cleaned_data.append(new_row)
    return jsonify({'events': cleaned_data})


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
    return jsonify({'data list': cleaned_data})


# Get data from a data object
# Used as 'GET /data?id=<dataID>'
@app.route('/data', methods=['GET'])
def get_data():
    data_id = request.args.get('id')
    query = get_data_query(data_id)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'sessionid', 'sessiondata', 'data_type']
    cleaned_data = {}
    for i, col in enumerate(list(data)):
        cleaned_data.update({columns[i]: col})
    return jsonify(cleaned_data)


"""
Session API Calls
"""


# Toggle (start/top) session for a set eventID
# Used as 'GET /toggle_session?id=<eventID>'
@app.route('/toggle_session', methods=['GET'])
def toggle_session():
    # Get student eventID and studentID
    event_id = request.args.get('id')
    student_id_query = get_event_student_id_query(event_id)
    student_id = list(execute_read_query(db, student_id_query)[0])[0]

    # Get other started eventIDs
    started_events_query = get_all_started_activities_query(student_id)
    started_events = [list(x)[0] for x in execute_read_query(db, started_events_query)]

    # If current event already started, set to paused, if not set to started
    if int(event_id) in started_events:
        new_status = 'paused'
        session_query = get_session_with_null_stop_time_query(event_id)
        session = list(execute_read_query(db, session_query)[0])[0]
        session_update_query = update_session_stop_time_query(session)
        execute_write_query(db, session_update_query)
    else:
        new_status = 'started'
        new_session_query = new_study_session_query(event_id)
        execute_write_query(db, new_session_query)

    # Update event status
    event_update_query = update_activity_status_query(event_id, new_status)
    execute_write_query(db, event_update_query)

    for event in started_events:
        if event != int(event_id):
            # Update status of other events
            current_event_update_query = update_activity_status_query(event, 'paused')
            execute_write_query(db, current_event_update_query)

            # Get sessions and set stop time if needed
            sessions_query = get_session_with_null_stop_time_query(event)
            sessions = execute_read_query(db, sessions_query)

            for session in sessions:
                current_session = list(session)[0]
                session_update_query = update_session_stop_time_query(current_session)
                execute_write_query(db, session_update_query)

    return jsonify({'new status': new_status})


# Check if a session has been started for a studentID
# Used as 'GET /check_session?id=<studentID>'
@app.route('/check_session', methods=['GET'])
def check_session():
    session_id = None
    status = 'stopped'

    student_id = request.args.get('id')
    events_query = get_all_started_activities_query(student_id)
    events = execute_read_query(db, events_query)

    if len(events) == 1:
        event = list(events[0])[0]
        session_id_query = get_session_with_null_stop_time_query(event)
        session_id = list(execute_read_query(db, session_id_query)[0])[0]
        status = 'running'

    return jsonify({'status': status, 'id': session_id})


# Stop the session
# Used as 'GET /stop_activity?id=<eventID>'
@app.route('/stop_activity', methods=['GET'])
def stop_session():
    event_id = request.args.get('id')

    event_status_query = get_study_event_query(event_id)
    status = list(execute_read_query(db, event_status_query)[0])

    event_update_query = update_activity_status_query(event_id, 'completed')
    execute_write_query(db, event_update_query)

    if 'started' in status:
        session_query = get_session_with_null_stop_time_query(event_id)
        session = list(execute_read_query(db, session_query)[0])[0]

        session_update_query = update_session_stop_time_query(session)
        execute_write_query(db, session_update_query)

    return jsonify({'new status': 'completed'})


# Upload data belonging to a session, usualy after the session is stopped
# Used as 'POST /upload_data {data_type, sessiondata, sessionid}'
@app.route('/upload_data', methods=['POST'])
def upload_data():
    if not request.json:
        abort(400)
    data = request.json

    query = new_data_query(data['sessionid'], data['sessiondata'],
                           data['data_type'])
    execute_write_query(db, query)

    return jsonify(data)


# Update the note field for a set event
# Used as 'POST /event_notes {'id': <event_id>, 'notes': <notes>}'
@app.route('/event_notes', methods=['POST'])
def update_event_notes():
    if not request.json:
        abort(400)
    data = request.json

    query = update_activity_notes_query(data['id'], data['notes'])
    execute_write_query(db, query)

    return jsonify(data)


"""
Posting New Data API Calls
"""


# Create a new study event
# Used as 'POST /event {studentID, moduleID, teacherID, title, description,
# category, notes, status}'
@app.route('/event', methods=['POST'])
def new_study_event():
    # Check if request is a json object
    if not request.json:
        abort(400)
    data = request.json

    # Convert teacher short name into teacher id
    teacherid_query = get_teacher_id_from_short_query(data['teacherid'])
    teacherid = str(execute_read_query(db, teacherid_query)[0][0])
    data['teacherid'] = teacherid

    # Create query and execute it
    query = new_study_event_query(data)
    if query != 'ERROR':
        execute_write_query(db, query)
        return jsonify(data)
    else:
        return jsonify({'error': 'Invalid data entered'})


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
    return jsonify(post)


# Test if get requests are working with passing variables
# Used as 'GET /testing_get?var=<test_variable>'
@app.route('/testing_get', methods=['GET'])
def test_get():
    var = request.args.get('var')
    return var


"""
Start Server
"""

if __name__ == '__main__':
    remove('database.sqlite3')
    print('Starting StudyBuddy Server...')

    print('Initializing database...')
    i = 0
    while not check_db():
        i += 1
        print('Database not found, creating new database...')
        create_db(1)
        if i >= 5:
            print('Error: cannot create database!')
            exit()
    db = initialize_db()
    print('Database initialized...')

    print('Starting Flask application...')
    app.static_folder = 'static'
    app.run(host='0.0.0.0')
