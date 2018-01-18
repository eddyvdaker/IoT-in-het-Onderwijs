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
def create_db():
    db = connect(DB_SETTING.get('database', 'file_name'))
    db_cursor = db.cursor()
    commands = [
        """
        CREATE TABLE teacher(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            name 			TEXT NOT NULL
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
            time_est		TEXT,
            
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
    db.close()


# Initialize database
def initialize_db():
    return connect(DB_SETTING.get('database', 'file_name'))


def execute_query(db, command):
    db_cursor = db.cursor()
    db_cursor.execute(command)
    db.commit()
