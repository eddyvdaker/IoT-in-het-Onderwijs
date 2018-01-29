"""
Contains any additional code needed to create the StudyBuddy Dashboard
"""

from datetime import datetime, timedelta

from database import *
from queries import *


# Generate page_vars to show on the students page
def get_student_page_vars(username, db):
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

    return page_vars


# Generate page_Vars to show on activity page
def get_activity_page_vars(activity, db):
    # Get Activity Information
    query = get_study_event_query(activity)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    page_vars = {}
    for i, col in enumerate(data):
        if i == 9:
            col = timedelta(minutes=int(col))

        page_vars.update({columns[i]: col})

    page_vars.update({'username': page_vars['studentid']})

    # Get Sessions Information
    session_query = get_session_information(activity)
    session_data = execute_read_query(db, session_query)
    session_columns = ['id', 'activityid', 'starttime', 'stoptime', 'date']

    sessions_value = []
    time_taken = 0
    for session in session_data:
        session_value = {}
        for i, col in enumerate(list(session)):
            if (i == 2 or i == 3) and col:
                col = datetime.fromtimestamp(int(col)).strftime('%H:%M')
            elif i == 4:
                col = datetime.fromtimestamp(int(list(session)[2])).strftime('%Y-%m-%d')

            session_value.update({session_columns[i]: col})

        if session[3]:
            time_taken += int(session[3]) - int(session[2])
        sessions_value.append(session_value)

    page_vars.update({'sessions': sessions_value, 'time': timedelta(seconds=time_taken)})

    data_value = []
    data_columns = ['id', 'sessionid', 'data', 'datatype']
    # Get All Data for Activity
    for session in sessions_value:
        data_for_session_query = get_data_for_session(session['id'])
        session_data = execute_read_query(db, data_for_session_query)

        for row in session_data:
            row_dict = {}
            for i, col in enumerate(list(row)):
                row_dict.update({data_columns[i]: col})
            data_value.append(row_dict)

    page_vars.update({'data': data_value})

    return page_vars
