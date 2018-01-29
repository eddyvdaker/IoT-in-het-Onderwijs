"""
Contains any additional code needed to create the StudyBuddy Dashboard
"""

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
    query = get_study_event_query(activity)
    data = list(execute_read_query(db, query)[0])
    columns = ['id', 'studentid', 'moduleid', 'teacherid', 'title',
               'description', 'category', 'notes', 'activity_status',
               'time_est']
    page_vars = {}
    for i, col in enumerate(data):
        page_vars.update({columns[i]: col})

    page_vars.update({'username': page_vars['studentid']})

    return page_vars
