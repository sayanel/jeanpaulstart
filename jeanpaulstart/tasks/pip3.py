from copy import deepcopy
from subprocess import call
from jeanpaulstart.constants import *


TASK_COMMAND = 'pip3'


def validate(user_data):
    return OK, ""


def normalize_after_split(splitted):
    normalized = deepcopy(splitted)
    normalized['arguments']['state'] = splitted['arguments'].get('state', STATE_PRESENT)
    return normalized


def apply_(name, state):

    command = "C:\\cube\\python3\\Scripts\\pip3 install {state}{name}".format(
        state='--upgrade ' if state == STATE_FORCE_REINSTALL else '',
        name=name
    )

    call(command, shell=True)
