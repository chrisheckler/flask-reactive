import os
from app import create_app

config_name = '/home/ubuntu/flask-reactive/instance/config.py'
app = create_app(config_name)

if __name__ == '__main__':
    {{app}}.run()
