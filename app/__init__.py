from config import app_config
from app.app import app

def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')
    app.secret_key = 'aKRRDonzGnboYJcx$ZXhDTn7H%Rh2hFsQKiDN9(NBPGdnr*Z@L5VfUZtaZ@i'
    app.config['SESSION_TYPE'] = 'filesystem'
    return app
