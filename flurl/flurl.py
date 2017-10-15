from flask import Flask

# Create the application instance.
app = Flask(__name__)

# Additionally load config from the environment variable.
app.config.from_envvar('FLURL_SETTINGS', silent=True)
