import sqlite3

from flask import Blueprint, g, current_app


def connect_db():
    '''
    Connect to the database specified in the config.
    '''

    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    '''
    Open a new database connection if there is none yet for the
    current application context.
    '''

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()


def init_db():
    '''
    Initialise the database by reading the schema file.
    '''

    db = get_db()

    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()
