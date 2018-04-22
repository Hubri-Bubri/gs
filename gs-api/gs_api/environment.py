from os.path import dirname, abspath
from gs_configurator import Configurator


APPLICATION_DIR = dirname(abspath(__file__))
resources_dir = f'{APPLICATION_DIR}/resources'
config_file_name = 'gs-api.yaml'
config_file_dirs = '/etc/gs', '/opt/gs', APPLICATION_DIR

configuration = Configurator(config_file_name, config_file_dirs)
