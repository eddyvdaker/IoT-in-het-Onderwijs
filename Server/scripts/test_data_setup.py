"""
Script that generates a bunch of test data and writes it to the database.
There is no way to undo these changes, and this script should thus only
be used in testing environments and not in production.
"""

from os import path
from pathlib import Path
from sqlite3 import connect


db_file = Path(f'{path.abspath("")}/../database.sqlite3')

# Check if db file exists
if not db_file.is_file():
    print('Database does not exist, run the server once first...')
    exit()

# Connect to db file
db = connect(str(db_file))
db_cur = db.cursor()

commands = ["INSERT INTO teacher (name) VALUES ('test_docent1');",
            "INSERT INTO teacher(name) VALUES('test_docent2');",
            "INSERT INTO student (name) VALUES ('test_student1');",
            "INSERT INTO student (name) VALUES ('test_student2');",
            "INSERT INTO lesson_module (id, name, description) VALUES ('tm01', 'test_module1', 'First testing module');",
            "INSERT INTO lesson_module (id, name, description) VALUES ('tm02', 'test_module2', 'Second testing module');",
            "INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, status, time_est) VALUES (1, 'tm01', 2, 'Test activity 1', 'First testing activity for student1', 'Reading', 'This is part of test data', 'not started', '30');",
            "INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, status, time_est) VALUES (1, 'tm02', 1, 'Test activity 2', 'Second testing activity for student1', 'Class', 'This is part of test data', 'started', '50');",
            "INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, status, time_est) VALUES (2, 'tm02', 1, 'Test activity 3', 'First testing activity for student2', 'Assignment', 'This is part of test data', 'started', '120');",
            "INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, status, time_est) VALUES (2, 'tm02', 1, 'Test activity 1', 'Second testing activity', 'Class', 'This is part of test data', 'completed', '15');",
            "INSERT INTO study_session (eventid, start_time, stop_time, collected_data, date) VALUES (2, '15:35', '15:40', '{keys: [\"a\", \"b\", \"c\"], windows: [\"win1\", \"win2\"], temperature: [25, 24, 24, 24, 25, 26, 24]}', '2018-01-17' );",
            "INSERT INTO study_session (eventid, start_time, stop_time, collected_data, date) VALUES (2, '15:45', '16:15', '{keys: [\"e\", \"f\"], windows: [\"win1\", \"win3\"], temperature: [24, 25, 26, 24]}', '2018-01-17');",
            "INSERT INTO study_session (eventid, start_time, date) VALUES (3, '20:00', '2018-01-17' );",
            "INSERT INTO study_session (eventid, start_time, stop_time, collected_data, date) VALUES (4, '11:10', '12:30', '', '2018-01-17' );",
            "INSERT INTO study_session (eventid, start_time, stop_time, collected_data, date) VALUES (2, '08:50', '10:00', '{keys: [\"a\", \"b\", \"c\"], windows: [\"win1\"], humidity: [33, 32, 32, 34]}', '2018-12-12' );"]

for command in commands:
    db_cur.execute(command)
db.commit()
db.close()

print('Test data written to db...')
