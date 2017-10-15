import os

from flask import Flask, g
from secrets import token_urlsafe

from .db import init_db


def create_app(config=None):
    '''
    Application factory to create the application with the ability
    to provide additional configuration from the config argument.
    '''

    app = Flask(__name__)

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'flurl.db'),
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLURL_SETTINGS', silent=True)

    register_cli(app)
    register_teardowns(app)

    return app



def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        '''
        CLI command to initialise the database, usage:
            $ flask initdb
        '''

        init_db()
        print('Initialised the database.')


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        '''
        Close the database at the end of the request.
        '''

        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


def generate_url(length=4):
    '''
    Generate a random URL string with a default length of 4.
    '''

    shortened = token_urlsafe(length)
    return shortened
