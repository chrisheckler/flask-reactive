import os
from subprocess import call

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

from charmhelpers.core import unitdata, hookenv

from lib.charms.layer.flask_reactive import (
    FLASK_HOME,
    render_flask_secrets,
)

from charmhelpers.contrib.charmsupport.volumes import get_config

from charms.layer.flask_reactive import configure_site

from charmhelpers.contrib.python.packages import pip_install_requirements

from charmhelpers.core.hookenv import charm_dir

@when_not('flask-reactive.installed')
def install_and_create_dir():
    """Flask dir created for config, etc.
       Install Flask/supplemental packages.
    """

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
             'SECRET_KEY': os.urandom(16),
           }

    render_flask_secrets(ctxt)

    status_set('active', 'Flask config rendered')
    log('Flask config rendered')
    set_flag('flask-reactive.secrets.available')


@when('nginx.available')
@when_not('nginx.configured')
def nginx_configure():
    """Configures NGINX to flask-reactive"""

    status_set('active', 'Configuring Nginx')

    configure_site('flask-reactive', 'vhost.conf', 
                   app_path='/home/ubuntu/flask')

    log('Nginx Configured')
    status_set('active', 'Nginx Cconfigured')
    set_flag('nginx.configured')
