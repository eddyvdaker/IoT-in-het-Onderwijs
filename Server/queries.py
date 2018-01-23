"""
Generates different queries needed to get the relevant data.
"""


"""
Direct API Call Queries
"""


def get_study_events_list_query(student_id):
    return f'SELECT id FROM study_activity WHERE studentid = {student_id};'


def get_study_event_query(event_id):
    return f'SELECT * FROM study_activity WHERE id = {event_id};'


def get_study_events_query(student_id):
    return f'SELECT * FROM study_activity WHERE studentid = {student_id};'


def get_study_sessions_query(event_id):
    return f'SELECT id FROM study_session WHERE activityid = {event_id}'


def get_study_session_query(session_id):
    return f'SELECT * FROM study_session WHERE id = {session_id}'


def get_data_list_query(session_id):
    return f'SELECT id FROM session_data WHERE sessionid = {session_id}'


def get_data_query(data_id):
    return f'SELECT * FROM session_data WHERE id = {data_id}'


def toggle_session_query(event_id):
    return f'DB QUERY'


def check_session_query(student_id):
    return f'DB QUERY'


def new_study_event_query(json_object):
    return f'DB QUERY'
