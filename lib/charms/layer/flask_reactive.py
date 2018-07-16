import os
from subprocess import call
import toml

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from charmhelpers.core import unitdata, hookenv, host

from charmhelpers.core.hookenv import charm_dir, status_set, log

from charmhelpers.contrib.python.packages import pip_install_requirements

from charmhelpers.core.templating import render

from charmhelpers.core.host import (
    service_stop,
    service_start,
    service_restart,
    service_running,
)


FLASK_HOME = "/home/ubuntu/flask"
SECRETS = os.path.join(FLASK_HOME, 'config.py')

kv = unitdata.kv()


def load_template(name, path=None):
    """Load template file for rendering config."""

    if path is None:
        path = os.path.join(charm_dir(), 'templates')
    env = Environment(
        loader=FileSystemLoader(path))

    return env.get_template(name)


def render_flask_secrets(secrets=None):
    """Renders flask secrets from template."""

    if secrets:
        secrets = secrets
    else:
        secrets = {}

    if os.path.exists(SECRETS):
        os.remove(SECRETS)

    app_yml = load_template('flask-config.py.j2')
    app_yml = app_yml.render(secrets=return_secrets(secrets))

    spew(SECRETS, app_yml)
    os.chmod(os.path.dirname(SECRETS), 0o755)


def spew(path, data):
    """Writes data to path."""

    with open(path, 'w+') as f:
        f.write(data)


def return_secrets(secrets=None):
    """Return sercrets dictionar."""

    if secrets:
        secrets_mod = secrets
    else:
        secrets_mod = {}

    return secrets_mod


def load_site():
    if not os.path.isfile('site.toml'):
        return {}

    with open('site.toml') as fp:
        conf = toml.loads(fp.read())

    return conf


def load_unitfile():
    """Loads unitfile.toml template"""

    if not os.path.isfile('unitfile.toml'):
        return {}
    with open('unitfile.toml') as fp:
        conf = toml.loads(fp.read()) 
        
    return conf


def config_nginx(site, template, **kwargs):
    """Configures nginx with site.toml and vhost.conf"""

    status_set('maintenance', 'Configuring site {}'.format(site))

    status_set('active', '')
    config = hookenv.config()
    context = load_site()
    context['host'] = config['host']
    context['port'] = config['port']
    context.update(**kwargs)
    conf_path = '/etc/nginx/sites-available/{}'.format(site)

    if os.path.exists(conf_path):
        os.remove(conf_path)
    render(source=template,
           target=conf_path,
           context=context)

    symlink_path = '/etc/nginx/sites-enabled/{}'.format(site)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)

    if os.path.exists('/etc/nginx/sites-enabled/default'):
        os.remove('/etc/nginx/sites-enabled/default')

    os.symlink(conf_path, symlink_path)
    log(context)


def stop_flask():
    """Stops flask service"""

    if host.service_running('flask_reactive'):
        host.service_stop('flask_reactive')
    call(['systemctl', 'disable', 'flask_reactive'])
    if os.path.exists('etc/systemd/system/flask_reactive.service'):
        os.remove('/etc/systemd/system/flask_reactive.service')


def start_flask_gunicorn(path, app, port, workers):
    """Configures and starts gunicorn"""

    stop_flask()
    path = path.rstrip('/')
    info = path.rsplit('/', 1)
    main = info[1].split('.', 1)[0]

    if os.path.exists(info[0] + '/wsgi.py'):
        os.remove(info[0] + '/wsgi.py')
    render(source='gunicorn.wsgi',
           target=info[0] + '/wsgi.py',
           context={
               'app': app,
               'main': main,
           })
    unitfile_dict = load_unitfile()
    unitfile_context = {**unitfile_dict}
    unitfile_context['port'] = str(port)
    unitfile_context['pythonpath'] = info[0]
    unitfile_context['app'] = app
    unitfile_context['workers'] = str(workers)
    render(source=load_template('unitfile.toml'),
           target='/etc/systemd/system/{}.service'.format(app),
           context=unitfile_context)

    call(['systemctl', 'enable', '{}'.format(app)])


