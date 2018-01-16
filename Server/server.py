"""
StudyBuddy Server
"""

from flask import Flask

from database import *
from queries import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    pass


"""
Retrieving data
"""


# Get a list of study events for a certain student ID
# Used as 'GET /events?id=<studentID>'
@app.route('/events', methods=['GET'])
def get_study_events():
    pass


# Get details of a specific study event, contains a list of sessions
# Used as 'GET /event?id=<eventID>'
@app.route('/event', methods=['GET'])
def get_study_event():
    pass


# Get details of a session, includes the data generated for that session
# Used as 'GET /session?id=<sessionID>'
@app.route('/session', methods=['GET'])
def get_study_session():
    pass


"""
Posting new data
"""


# Create a new study event
# Used as 'POST /event {studentID, moduleID, teacherID, title, description,
# category, notes, status}'
@app.route('/event', methods=['POST'])
def new_study_event():
    pass


# Start a new study session
# Used as 'POST /start_session {eventID, start time, date}
@app.route('/start_session', methods=['POST'])
def start_study_session():
    pass


# Stop a currently ongoing study session
# Used as 'POST /stop_session {eventID, stop time, date, collected data}
@app.route('/stop_session', methods=['POST'])
def stop_study_session():
    pass


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
