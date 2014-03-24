# -*- coding: utf-8 -*-
from os.path import join, exists
import os
import sys
import yaml
import logging

from .singleton import Singleton


DEFAULT_CONFIG_DIR = 'config'
DEFAULT_CONFIG_FILE = 'config.yml'

REVISION_FILE = 'REVISION'
TIMESTAMP_FILE = 'TIMESTAMP'


class Configurator(Singleton):
    """Application settings manager


    This class is used for the storage and the usage of all the application
    configuration settings. The object is a singleton in the current
    WSGI thread scope.

    Constructor takes a hint for the location, and loads all configuration.
    It should be one of the first things called called in the initialization
    file (usually main.py) since app-specific packages may try to read the
    configuration. Most of the time (`config` folder alonside `main.py`) that
    call should do it:

    >>> from os import path
    >>> from lib.common import Configurator
    >>> Configurator(path.dirname(path.realpath(__file__)))

    Please note that the second line ought to change depending on how this
    project is included.
    Sub-sequent instantiations have no reason not to be parameter-less.

    In case where no hint is given, it will try to look in the current directory
    and the path folders before giving up.

    Parameters
    ----------
    root : string
        Root directory of the application, containing a 'config' folder.
        Either `root` or `config_dir` must be provided on first call.
    config_dir : string
        Root directory of the configuration.
    """
    def __init__(self, root=None, config_dir=None):
        self.config_dir = config_dir
        self.settings = {}

        if not (root is None) ^ (config_dir is None):
            logging.critical("Must give either root or config_dir on first call")

            if root is None:
                # nothing given, try to find a suitable folder
                root = self.try_find_config_dir()
                if root is None:
                    logging.critical("No configuration folder could be found." +
                                     " The application may be unstable.")
                    return

        if root is not None:
            self.config_dir = join(root, DEFAULT_CONFIG_DIR)

        self.read_configuration(self.config_dir)
        self.boe_header = self.build_header()

    def build_header(self):
        """Build X-Boe-Header value"""
        import socket
        hostname = socket.gethostname()
        return '%s' % hostname

    def try_find_config_dir(self):
        """Try to find a config folder in the path/cwd

        This is a last-recourse solution, and may be useful with tools like
        nosetests, but is fundamentally weak and dangerous"""
        candidates = list(sys.path)
        candidates.append(os.getcwd())
        for c in candidates:
            if exists(join(c, DEFAULT_CONFIG_DIR)):
                logging.info("Found a config folder in %s", c)
                return c

    def read_file(self, filename):
        """Read configuration file and parse the yaml

        filename : str
            Full path to the configuration file"""
        logging.info("Reading configuration file %s", filename)
        try:
            with open(filename) as configuration_file:
                return yaml.load(configuration_file) or {}
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            logging.warning("Configuration file %s is not a valid yaml file", filename)
        except IOError:
            logging.warning("Could not open file %s", filename)
        return {}

    def reload(self):
        """
        Reload the config file.

        Should happen after CONFIG_FILE env variable is changed.
        """
        self.read_configuration(self.config_dir)

    def read_configuration(self, config_dir):
        """Read the configuration file.

        Should only happens once per thread.
        To allow config file overide (e.g. on integration tests), one should override the CONFIG_FILE env variable
        """
        config_file = os.getenv('CONFIG_FILE', DEFAULT_CONFIG_FILE)
        self.settings = self.read_file(join(config_dir, config_file))

    def get_setting(self, setting, default=17889350):
        """Get a setting

        If `setting` is not available and no default is provided a KeyError is raised

        Parameters
        ----------
        setting : str
            Name of the desired setting parameter
        default : object, optional
            Default value, can be None
        """
        # magic value here to allow None
        if default != 17889350:
            return self.settings.get(setting, default)
        return self.settings[setting]

    def get_settings(self):
        """Return all settings"""
        return dict(self.settings)

    def get(self, value, default=None):
        return self.settings.get(value, default)

    def __getitem__(self, key):
        return self.settings[key]

    def find(self, keys, default=None):
        """Recursive lookup ok `keys` elements in sub-settings

        If `keys` is "a.b.c.d." then this is similar to config["a"]["b"]["c"]["d"].
        If there is any problem on the way, `default` will be returned

        Parameters
        ----------
        keys : str
            `keys` elements must be separated by a '.', e.g. 'param.subparam.subsubparam'
        default : object, optional
            default value to return if an element is not found. Cannot be None.
        """
        elem = self
        for key in keys.split('.'):
            try:
                elem = elem[key]
            except KeyError:
                return default
            except TypeError:
                break
        if elem is self:
            return default
        return elem