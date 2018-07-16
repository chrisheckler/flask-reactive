import os
from subprocess import call
import toml

from charms.reactive import (
    when,
    when_not,
    set_flag,
    clear_flag,
    endpoint_from_flag,
)

from charmhelpers.core.hookenv import (
    status_set,
    log,
    open_port,
)

from charmhelpers.core.host import (
    service_stop,
    service_start,
    service_restart,
    service_running,
)

from charmhelpers.core import unitdata, hookenv, host

from lib.charms.layer.flask_reactive import (
    FLASK_HOME,
    render_flask_secrets,
    stop_flask,
    config_nginx,
    start_flask_gunicorn,
    load_template,
    load_unitfile,
)

from charmhelpers.contrib.charmsupport.volumes import get_config

from charmhelpers.contrib.python.packages import pip_install_requirements

from charmhelpers.core.hookenv import charm_dir

config = hookenv.config()


@when_not('flask-reactive.installed')
def install_and_create_dir():
    """Flask dir created for config, etc.
       Install Flask/supplemental packages.
    """

    if not os.path.exists(FLASK_HOME):
        os.mkdir(FLASK_HOME)

    if not os.path.exists(FLASK_HOME):
        os.mkdir(FLASK_HOME)

    packages = ['Flask', 'Flask-API', 'Flask-Migrate', 'gunicorn',
                'Flask-Script', 'Flask-SQLAlchemy', 'SQLAlchemy']

    for pkg in packages:
        call(['pip', 'install', '-U', pkg])

    log('Flask packages have been installed')
    status_set('active', 'Flask and supporting packages installed')
    set_flag('flask-reactive.installed')


@when('flask-reactive.installed')
@when_not('flask-reactive.secrets.available')
def render_secrets():
    """Write out flask secrets."""
    
    status_set('active', 'Rendering flask-reactive config')

    ctxt = {
             'DEBUG': False,
             'TESTING': False,
             'SECRET': os.urandom(16),
           }

    render_flask_secrets(ctxt)

    status_set('active', 'Flask config rendered')
    log('Flask config rendered')
    set_flag('flask-reactive.secrets.available')


@when('nginx.available')
@when_not('flask.nginx.configured')
def nginx_configure():
    """Configures NGINX to flask-reactive"""

    status_set('active', 'Configuring Nginx')

    config_nginx('flask-reactive', 'vhost.conf',
                 app_path='/home/ubuntu/flask')

    log('Nginx Configured')
    status_set('active', 'Nginx Cconfigured')
    set_flag('flask.nginx.configured')


@when('flask.nginx.configured')
@when_not('flask.gunicorn.ready')
def flask_gunicorn_configure():
    """Configuring gunicorn"""
    
    status_set('active', 'Starting Flask-reactive')

    stop_flask()
    start_flask_gunicorn('/home/ubuntu/flask', 'flask-reactive', 
                         config['port'], config['workers'],
                         load_unitfile('unitfile.toml'))
    status_set('active', 'Flask-reactive initialized')
    set_flag('flask.gunicorn.ready')
