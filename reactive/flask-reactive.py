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

from charmhelpers.core import unitdata

from lib.charms.layer.flask_reactive import (
    FLASK_HOME,
)


@when_not('flask-reactive.installed')
def install_and_create_dir():
    """Flask dir created for config, etc.
       Install Flask/supplemental packages.
    """

    if not os.path.exists(FLASK_HOME):
        os.mkdir(FLASK_HOME)

    packages = ['Flask', 'Flask-API', 'Flask-Migrate',
                'Flask-Script', 'Flask-SQLAlchemy', 'SQLAlchemy']

    for pkg in packages:
        call(['pip', 'install', '-U', pkg])

    log('Flask packages have been installed')
    status_set('active', 'Flask and supporting packages installed')
    set_flag('flask-reactive.installed')


@when('flask-reactive.installed')
@when_not('flask-reactive.secrets.available')
def render_flask_secrets():
    """Write out flask secrets
    """

    status_set('active', 'Rendering flask-reactive config')

    ctxt = {
            "DEBUG": False,
            "TESTING": FLASK_HO
            "SECRET_KEY": os.urandom(16)
            }
