"""
This script tests the functionality of the toggle_session API call.
For correct results run this against the test data as generated by
database.py.
"""

import json
import urllib.request
import urllib.error

# Helper VARS
host = '127.0.0.1'
base_url = f'http://{host}:5000'

# Test VARS
student_ids = [1, 2]
activity_ids = [1, 2, 3]
session_ids = [1, 2, 3, 4]
session_ids2 = [1, 2, 3, 4, 5]

print('')


"""
HELPER FUNCTIONS
"""


# Generate correct url for API call and ID
def generate_url(call, id):
    return f'{base_url}/{call}?id={id}'


# Send request, and convert reply into JSON
def req(call, id):
    url = generate_url(call, id)
    reply = urllib.request.urlopen(url)
    content = reply.read().decode('utf-8')
    return json.loads(content)


"""
TEST FUNCTIONS
"""


# Student IDs to check and expected values in a dict.
def events_status(ids, expected_values):
    test_status = ' OK'
    error = ''

    for id in ids:
        data = req('events', id)
        values = [x['activity_status'] for x in data['events']]
        if values != expected_values[id]:
            test_status = ''
            error += f' ERROR: {values} is not {expected_values[id]} as expected (id = {id})'

    return f'STATUS -{test_status}{error}'


def sessions_list_status(ids, expected_values):
    test_status = ' OK'
    error = ''

    for id in ids:
        data = req('sessions', id)
        values = data['sessions']
        if values != expected_values[id]:
            test_status = ''
            error += f' ERROR: {values} is not {expected_values[id]} as expected (id = {id})'

    return f'STATUS -{test_status}{error}'


def session_details_status(ids, expected_values):
    test_status = ' OK'
    error = ''

    for id in ids:
        try:
            data = req('session', id)
            values = data['stop_time']
        except urllib.error.HTTPError:
            values = 'Server Error!'

        if values == 'Server Error!':
            test_status = ''
            error += f' ERROR: {values} (id = {id})'
        elif expected_values[id] == '<SOME_TIME>':
            if not values:
                test_status = ''
                error += f' ERROR: stop_time is {values} instead of a timestamp as expected (id = {id})'
        elif values != expected_values[id]:
            test_status = ''
            error += f' ERROR: {values} is not {expected_values[id]} as expected (id = {id})'

    return f'STATUS -{test_status}{error}'


def toggle_session_status(ids, expected_value):
    test_status = ' OK'
    error = ''

    data = req('toggle_session', ids)
    value = data['new status']

    if value != expected_value:
        test_status = ''
        error += f' ERROR: {value} is not {expected_value}'

    return f'STATUS -{test_status}{error}'


"""
RUNNING TESTS
"""

# TEST 1    - CHECK ACTIVITY STATUS BEFORE TOGGLE
t1 = events_status(student_ids, {1: ['not started', 'started'], 2: ['started', 'completed']})
print(f'1. \tCheck activity status before toggle \t- {t1}')

# TEST 2    - CHECK SESSION LISTS BEFORE TOGGLE
t2 = sessions_list_status(activity_ids, {1: [1], 2: [2], 3: [3, 4]})
print(f'2. \tCheck session lists before toggle \t\t- {t2}')

# TEST 3    - CHECK SESSION DETAILS BEFORE TOGGLE
t3 = session_details_status(session_ids, {1: '15:35', 2: None, 3: '01:00', 4: None})
print(f'3. \tCheck session details before toggle \t- {t3}')

# TEST 4    - TOGGLE SESSION FOR ACTIVITY 1
t4 = toggle_session_status(1, 'started')
print(f'4. \tCheck toggle status \t\t\t\t\t- {t4}')

# TEST 5    - CHECK ACTIVITY STATUS AFTER TOGGLE 1
t5 = events_status(student_ids, {1: ['started', 'paused'], 2: ['started', 'completed']})
print(f'5. \tCheck activity status after toggle 1 \t- {t5}')

# TEST 6    - CHECK SESSION LISTS AFTER TOGGLE 1
t6 = sessions_list_status(activity_ids, {1: [1, 5], 2: [2], 3: [3, 4]})
print(f'6. \tCheck session lists after toggle 1 \t\t- {t6}')

# TEST 7    - CHECK SESSION DETAILS AFTER TOGGLE 1
t7 = session_details_status(session_ids2, {1: '15:35', 2: '<SOME_TIME>', 3: '01:00', 4: None, 5: None})
print(f'7. \tCheck session details before toggle \t- {t7}')

# TEST 8    - TOGGLE SESSION FOR ACTIVITY 1 AGAIN
t8 = toggle_session_status(1, 'paused')
print(f'8. \tCheck toggle status \t\t\t\t\t- {t8}')

# TEST 9    - CHECK ACTIVITY STATUS AFTER TOGGLE 2
t9 = events_status(student_ids, {1: ['paused', 'paused'], 2: ['started', 'completed']})
print(f'9. \tCheck activity status after toggle 2 \t- {t9}')

# TEST 10   - CHECK SESSION LISTS AFTER TOGGLE 3
t10 = sessions_list_status(activity_ids, {1: [1, 5], 2: [2], 3: [3, 4]})
print(f'10. Check session lists after toggle 1 \t\t- {t10}')

# TEST 11   - CHECK SESSION DETAILS AFTER TOGGLE 4
t11 = session_details_status(session_ids2, {1: '15:35', 2: '<SOME_TIME>', 3: '01:00', 4: None, 5: '<SOME_TIME>'})
print(f'11. Check session details before toggle \t- {t11}')