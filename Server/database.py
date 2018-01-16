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
        CREATE TABLE module(
            id 				TEXT PRIMARY KEY NOT NULL,
            name 			TEXT NOT NULL,
            description 	TEXT NOT NULL
        );
        """, """
        CREATE TABLE activity(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            studentid 		INTEGER NOT NULL,
            moduleid 		TEXT NOT NULL,
            teacherid 		INTEGER NOT NULL,
            title 			TEXT NOT NULL,
            description 	TEXT,
            category 		TEXT,
            notes 			TEXT,
            status 			TEXT,

            FOREIGN KEY(studentid) REFERENCES student(id),
            FOREIGN KEY(moduleid) REFERENCES module(id),
            FOREIGN KEY(teacherid) REFERENCES teacher(id)
        );
        """, """
        CREATE TABLE session(
            id 				INTEGER PRIMARY KEY AUTOINCREMENT,
            eventid 		INTEGER NOT NULL,
            start_time 		TEXT NOT NULL,
            stop_time 		TEXT,
            collected_data 	TEXT,
            date 			TEXT NOT NULL,

            FOREIGN KEY(eventid) REFERENCES event(id)
        );"""]
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
