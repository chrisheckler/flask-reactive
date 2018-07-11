import os
import subprocess

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

from charms.layer.flaskhelpers import (
        install_requirements,
        start_api,
        restart_api,
        start,
        start_api_gunicorn,
        load_unitfile,
)

from charmhelpers.core import unitdata


PROJECT_PATH = "/home/ubuntu/"

@when_not('flask.installed')
def install():
    """ Install Flask 
    """
    status_set('active', 'Application Installed')
    log('Flask installed')
    set_flag('app.installed')

