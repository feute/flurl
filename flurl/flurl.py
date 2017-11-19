import os
import validators

from flask import Flask, g, request, redirect
from secrets import token_urlsafe

from .db import init_db, save_url, fetch_url


usage = """flurl is a simple URL shortener.

It is as simple as posting your URL to / and getting your shortened URL
as the response.

usage: curl -X POST -d <your-url> http://<server-url>/
"""

def create_app(config=None):
    """Application factory to create the application with the ability to
    provide additional configuration from the config argument.
    """
    app = Flask(__name__)

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'flurl.db'),
        MAX_URL_LENGTH=100,
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLURL_SETTINGS', silent=True)

    register_cli(app)
    register_teardowns(app)
    register_routes(app)

    return app



def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        """CLI command to initialise the database.
        Usage:
            $ flask initdb
        """
        init_db()
        print('Initialised the database.')


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        """Close the database at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


def register_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if not request.content_length:
                return 'No URL was provided.\n'
            if request.content_length > app.config['MAX_URL_LENGTH']:
                return 'Content is too long.\n'

            original_url = request.get_data(cache=False, as_text=True)
            if not validators.url(original_url):
                return 'Invalid URL.\n'

            shortened_url = generate_url()
            save_url(original_url, shortened_url)
            return request.url_root + shortened_url + '\n'

        return usage


    @app.route('/<short_url>')
    def redirect_url(short_url):
        original_url = fetch_url(short_url)
        if not original_url:
            return "The URL doesn't exist.\n"

        return redirect(original_url)


def generate_url(length=4):
    """Generate a random URL string with a default length of 4."""
    shortened = token_urlsafe(length)
    return shortened
