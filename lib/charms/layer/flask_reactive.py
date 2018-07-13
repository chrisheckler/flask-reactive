import os

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from charmhelpers.core import unitdata
from charmhelpers.core.hookenv import charm_dir

FLASK_HOME = "/home/ubuntu/flask"
FLASK_SECRETS = os.path.join(FLASK_HOME, 'flask_secrets', 'flask_secrets.py')

kv = unitdata.kv()


def load_template(name, path=None):
    """Load template file for rendering config
    """

    if path is None:
        path = os.path.join(charm_dir(), 'templates')
    env = Environment(
        loader=FileSystemLoader(path))

    return env.get_template(name)


def render_flask_secrets(secrets=None):
    """Renders flask secrets from template
    """

    if secrets:
        secrets = secrets
    else:
        secrets = {}

    if os.path.exists(FLASK_SECRETS):
        os.remove(FLASK_SECRETS)

    app_yml = load_template('flask_secrets.py.j2')
    app_yml = app_yml.render(secrets=return_secrets(secrets))

    spew(FLASK_SECRETS, app_yml)
    os.chmod(os.path.dirname(FLASK_SECRETS), 0o755)


def spew(path, data):
    """Writes data to path
    """

    with open(path, 'w+') as f:
        f.write(data)


def return_secrets(secrets=None):
    """Return sercrets dictionary
    """

    if secrets:
        secrets_mod = secrets
    else:
        secrets_mod = {}

    return secrets_mod
