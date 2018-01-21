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
    fields = [{'name': 'studentid', 'required': 1, 'type': 'int'},
              {'name': 'moduleid', 'required': 1, 'type': 'text'},
              {'name': 'teacherid', 'required': 1, 'type': 'int'},
              {'name': 'title', 'required': 1, 'type': 'text'},
              {'name': 'description', 'required': 0, 'type': 'text'},
              {'name': 'category', 'required': 0, 'type': 'text'},
              {'name': 'notes', 'required': 0, 'type': 'text'},
              {'name': 'activity_status', 'required': 1, 'type': 'text'},
              {'name': 'time_est', 'required': 0, 'type': 'int'}]

    fields_query = ''
    data_query = ''

    for i, field in enumerate(fields):
        if i != 0:
            fields_query += ', '
            data_query += ', '

        if field['name'] is 'activity_status':
            data_query += '\"not started\"'
        elif json_object[field['name']] is '':
            if field['required'] == 1:
                return 'ERROR'
            else:
                data_query += 'NULL'
        elif field['type'] is 'text':
            data_query += f'\"{json_object[field["name"]]}\"'
        else:
            data_query += str(json_object[field['name']])

        fields_query += field['name']

    return f'INSERT INTO study_activity ({fields_query}) VALUES ({data_query});'


def get_teacher_id_from_short_query(short):
    return f'SELECT id FROM teacher WHERE short = \'{short}\''
