import os

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


@when_not('app.installed')
def install():
    """ Install Flas requirements.txt
    """
    install_requirements(PROJECT_PATH + '/requirements.txt')
    status_set('active', 'Application Installed')
    log('Application requirements installed')
    set_flag('app.installed')
