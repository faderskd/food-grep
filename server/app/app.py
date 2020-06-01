from server.config.config import APP_PORT, APP_HOST
from server.app import app_factory


app, database = app_factory.create_app_with_dependencies(__name__)

if __name__ == '__main__':
    app.run(APP_HOST, APP_PORT)
