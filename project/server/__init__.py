from flask import Flask
from flask_cors import CORS
import os
from project.importer.importer import create_bucket

app : Flask = Flask(__name__)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# init couchbase connection
import json
from couchbase.admin import Admin
from couchbase.exceptions import HTTPError
from couchbase.cluster import Cluster, Bucket
from couchbase.cluster import PasswordAuthenticator
from couchbase.analytics import AnalyticsQuery

# Initialize couchbase connection and ensure required buckets exist
ip : str = 'localhost'
print('Connecting to Couchbase instance at %s' % (ip))

adm = Admin('Administrator', 'password', host=ip, port=8091)

create_bucket('media', 750, adm)
create_bucket('users', 100,adm)

adm._close()

# connect to buckets
cb_cluster : Cluster = Cluster('couchbase://localhost?operation_timeout=4')
authenticator : PasswordAuthenticator = PasswordAuthenticator('Administrator', 'password')
cb_cluster.authenticate(authenticator)
cb_media : Bucket = cb_cluster.open_bucket('media')
cb_users : Bucket = cb_cluster.open_bucket('users')

# register blueprints
from project.server.views.home import home_bp
app.register_blueprint(home_bp)

from project.server.views.titles import titles_bp
app.register_blueprint(titles_bp)

from project.server.views.search import search_bp
app.register_blueprint(search_bp)


def create_app():
    return app