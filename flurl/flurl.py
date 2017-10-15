import os

from flask import Flask, g

from .db import init_db

# Create the application instance.
app = Flask(__name__)

app.config.update(
    DATABASE=os.path.join(app.root_path, 'flurl.db'),
)

# Additionally load config from the environment variable.
app.config.from_envvar('FLURL_SETTINGS', silent=True)


@app.cli.command('initdb')
def initdb_command():
    '''
    CLI command to initialise the database, usage:
        $ flask initdb
    '''

    init_db()
    print('Initialised the database.')


@app.teardown_appcontext
def close_db(error):
    '''
    Close the database at the end of the request.
    '''

    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
