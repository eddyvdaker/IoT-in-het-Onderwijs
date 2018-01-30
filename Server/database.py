"""
Database interaction for the StudyBuddy Server
"""

from configparser import ConfigParser
from os import path
from pathlib import Path
from sqlite3 import connect

DB_SETTING = ConfigParser()
DB_SETTING.read(f'{path.abspath("")}/config/studybuddy_srv.conf')


# Check if database file exists
def check_db():
    file = Path(DB_SETTING.get('database', 'file_name'))
    return file.is_file()


# Create new database file
def create_db(debug):
    db = connect(DB_SETTING.get('database', 'file_name'))
    db_cursor = db.cursor()
    commands = [
        """
        CREATE TABLE teacher(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            name 			TEXT NOT NULL,
            short           TEXT NOT NULL
        );
        """, """
        CREATE TABLE student(
            id 				INTEGER PRIMARY KEY NOT NULL,
            name 			TEXT NOT NULL
        );
        """, """
        CREATE TABLE lesson_module(
            id 				TEXT PRIMARY KEY NOT NULL,
            name 			TEXT NOT NULL,
            description 	TEXT NOT NULL
        );       
        """, """
        CREATE TABLE study_activity(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            studentid 		INTEGER NOT NULL,
            moduleid 		TEXT NOT NULL,
            teacherid 		INTEGER,
            title 			TEXT NOT NULL,
            description 	TEXT,
            category 		TEXT,
            notes 			TEXT,
            activity_status TEXT NOT NULL,
            time_est		INTEGER,
            
            FOREIGN KEY(studentid) REFERENCES student(id),
            FOREIGN KEY(moduleid) REFERENCES lesson_module(id),
            FOREIGN KEY(teacherid) REFERENCES teacher(id)
        );
        """, """
        CREATE TABLE study_session(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            activityid 		INTEGER NOT NULL,
            start_time 		TEXT NOT NULL,
            stop_time 		TEXT,
            session_date 	TEXT NOT NULL,
            
            FOREIGN KEY(activityid) REFERENCES study_activity(id)
        );
        """, """
        CREATE TABLE session_data(
            id				INTEGER PRIMARY KEY AUTOINCREMENT,
            sessionid		INTEGER NOT NULL,
            sessiondata		TEXT,
            data_type		TEXT,
            
            FOREIGN KEY(sessionid) REFERENCES study_session(id)
        );
        """]
    for command in commands:
        db_cursor.execute(command)
    db.commit()

    if debug == 1:
        create_test_data(db)
    db.close()


# Initialize database
def initialize_db():
    return connect(DB_SETTING.get('database', 'file_name'))


def execute_write_query(db, command):
    db_cursor = db.cursor()
    db_cursor.execute(command)
    db.commit()


def execute_read_query(db, command):
    db_cursor = db.cursor()
    db_cursor.execute(command)
    return db_cursor.fetchall()


def create_test_data(db):
    commands = ["""
    INSERT INTO teacher (name, short) VALUES ('test_docent1', 'tt1');
    """, """
    INSERT INTO teacher (name, short) VALUES ('test_docent2', 'tt2');
    """, """
    INSERT INTO student (name) VALUES ('test_student1');
    """, """
    INSERT INTO student (name) VALUES ('test_student2');
    """, """
    INSERT INTO lesson_module (id, name, description) VALUES ('tm01', 'test_module1', 'First testing module');
    """, """
    INSERT INTO lesson_module (id, name, description) VALUES ('tm02', 'test_module2', 'Second testing module');
    """, """
    INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, activity_status, time_est) VALUES (1, 'tm01', 2, 'Werkcollege 1 week 4', 'Verdieping HC + start huiswerkopopdracht 2 (pi 7)', 'Werkcollege', 'Werkcollege en starten met huiswerkopdracht 2, het bouwen van een alarmsysteem.', 'not started', '30');
    """, """
    INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, activity_status, time_est) VALUES (1, 'tm02', 1, 'Zelfstudie reader week 4', 'Reader op blackboard lezen', 'Lezen', 'Lezen: business models for the internet of things', 'started', '50');
    """, """
    INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, activity_status, time_est) VALUES (2, 'tm02', 1, 'IoT Alarm afmaken', 'Afronden en testen IoT alarm systeem', 'Opdracht', 'Nieuwe functionaliteit getest', 'started', '120');
    """, """
    INSERT INTO study_activity (studentid, moduleid, teacherid, title, description, category, notes, activity_status, time_est) VALUES (2, 'tm02', 1, 'Hoorcollege week 1', 'Introductie hoorcollege week 1', 'Hoorcollege', 'Feedback op hoorcollege', 'completed', '15');
    """, """
    INSERT INTO study_session (activityid, start_time, session_date) VALUES (1, '1517234758', '2018-01-17');
    """, """
    UPDATE study_session SET stop_time = '1517235457' WHERE id = 1;
    """, """
    INSERT INTO study_session (activityid, start_time, session_date) VALUES (2, '1517238511', '2018-01-18');
    """, """
    INSERT INTO study_session (activityid, start_time, session_date) VALUES (3, '1517236872', '2018-01-20');
    """, """
    UPDATE study_session SET stop_time = '1517239546' WHERE id = 3;
    """, """
    INSERT INTO study_session (activityid, start_time, session_date) VALUES (3, '1517243783', '2018-01-25');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (1, '[["k", 1516287762.809912], ["j", 1516287762.9790134], ["f", 1516287763.1300404]]', 'Keystrokes');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (1, '["Window 1", 1516287756.1210876], ["Window 2", 1516287757.1222298]', 'Windows');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (1, '[22, 23, 22, 23, 24, 24, 24]', 'Temperature');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (2, '[["o", 1516287766.028941], ["1", 1516287766.178688], ["t", 1516287766.2447045], ["o", 1516287766.4024243]]', 'Keystrokes');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (2, '[["o", 1516287767.167402], ["space", 1516287767.1704023]]', 'Keystrokes');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (2, '[19, 18, 18, 18]' , 'Temperature');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (2, 'ts.guydols.nl:5000/videos/v1.mp4', 'Video');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (3, '[["6", 1516287762.6850154], ["shift", 1516287762.7680357], ["r", 1516287762.7828982], ["c", 1516287762.7848983], ["n", 1516287762.7919006]]', 'Keystrokes');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (3, '["Window 1", 1516287763.125039], ["Window 3", 1516287772.1310387]', 'Windows');
    """, """
    INSERT INTO session_data (sessionid, sessiondata, data_type) VALUES (3, '[25, 25, 25, 26, 27, 26]', 'Temperature');
    """]
    db_cursor = db.cursor()
    for command in commands:
        db_cursor.execute(command)
    db.commit()
