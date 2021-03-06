import os
import imp
import logging
from glob import glob
from collections import OrderedDict
import constants


loaded_plugins = OrderedDict()


class Loader(object):
    OK = constants.OK
    TASK_COMMAND_MISSING = "TASK_COMMAND_MISSING"
    TASK_COMMAND_NOT_STR = "TASK_COMMAND_NOT_STR"
    VALIDATE_MISSING = "VALIDATE_MISSING"
    NORMALIZE_MISSING = "NORMALIZE_MISSING"
    APPLY_MISSING = "APPLY_MISSING"

    def __init__(self, plugin_folder):
         self.plugin_folder = plugin_folder

    def list_names(self):
        search_path = os.path.join(self.plugin_folder, "*.py")
        files = glob(search_path)
        names = sorted([os.path.splitext(os.path.basename(file_))[0] for file_ in files])
        try:
            names.remove('__init__')
        except ValueError:
            pass

        logging.info("Listed {count:03d} plugins from : {plugin_folder}".format(
            count=len(names),
            plugin_folder=self.plugin_folder
        ))

        return names

    def make_plugin_filepath(self, plugin_name):
        return os.path.join(self.plugin_folder, plugin_name + '.py').replace('\\', '/')

    def load_by_filepath(self, plugin_filepath):
        if not os.path.isfile(plugin_filepath):
            return None

        name = os.path.splitext(os.path.basename(plugin_filepath))[0]

        return imp.load_source(name, plugin_filepath)

    def load_by_name(self, plugin_name):
        plugin_filepath = self.make_plugin_filepath(plugin_name)
        return self.load_by_filepath(plugin_filepath)

    def load(self, plugin_name=None, plugin_filepath=None):
        if plugin_name:
            return self.load_by_name(plugin_name)

        if plugin_filepath:
            return self.load_by_filepath(plugin_filepath)

    def validate(self, plugin):
        if not hasattr(plugin, "TASK_COMMAND"):
            return Loader.TASK_COMMAND_MISSING

        if not isinstance(plugin.TASK_COMMAND, str):
            return Loader.TASK_COMMAND_NOT_STR

        if not hasattr(plugin, "validate"):
            return Loader.VALIDATE_MISSING

        if not hasattr(plugin, "normalize_after_split"):
            return Loader.NORMALIZE_MISSING

        if not hasattr(plugin, "apply_"):
            return Loader.APPLY_MISSING

        return Loader.OK

    def load_all(self):
        plugins = OrderedDict()

        for plugin_name in self.list_names():

            plugin = self.load(plugin_name=plugin_name)
            status = self.validate(plugin)

            if status is not Loader.OK:
                logging.warn("Could not validate plugin : '{plugin_name}.py' ({status})".format(
                    plugin_name=plugin_name,
                    status=status
                ))
                continue

            command_name = plugin.TASK_COMMAND

            if command_name in plugins.keys():
                logging.warn("Skipping plugin '{plugin_name}.py' : command '{command_name}' already loaded".format(
                    plugin_name=plugin_name,
                    command_name=command_name
                ))
                continue

            plugins[command_name] = plugin

            logging.info("Successfully loaded plugin : '{plugin_name}.py'".format(plugin_name=plugin_name))

        return plugins


def init(plugin_folder=None, force=False):
    global loaded_plugins

    if plugin_folder is None:
        plugin_folder = os.path.expandvars('$PLUGIN_FOLDER')

    if plugin_folder == "$PLUGIN_FOLDER":
        import tasks
        plugin_folder=os.path.dirname(tasks.__file__)

    if loaded_plugins and not force:
        return False

    logging.info("Initializing plugins from {}".format(plugin_folder))

    loader = Loader(plugin_folder=plugin_folder)
    loaded_plugins = loader.load_all()

    return True
