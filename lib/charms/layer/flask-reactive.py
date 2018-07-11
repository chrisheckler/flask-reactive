import os
import json
import toml

from subprocess import call, Popen

from charms.reactive import set_state
from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render

config = hookenv.config()
