from ruamel.yaml import load as load_yml, RoundTripLoader
from os.path import isfile, dirname, abspath
from os import makedirs
import ruamel.yaml
import logging
from logging import FileHandler, StreamHandler, Formatter, getLevelName


logger = logging.getLogger(__name__)


class Configurator:
    _config = None
    _path = None
    _search_file = None
    _search_dirs = None
    _logger_format = None

    def __init__(self, search_file, search_dirs, logger_format=None):
        self._search_file = search_file
        self._search_dirs = search_dirs

    def _read_config_file(self, name, dirs):
        for fullname in [f'{dir}/{name}' for dir in dirs]:
            if isfile(fullname):
                with open(fullname, 'rt') as file:
                    return load_yml(file.read(), RoundTripLoader), fullname
        
        raise RuntimeError(f"config file not found in - {', '.join(dirs)}")

    def load(self):
        self._config, self._path = self._read_config_file(self._search_file, self._search_dirs)
        
    def __getitem__(self, key):
        return self._config[key]
