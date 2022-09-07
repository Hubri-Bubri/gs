from os.path import dirname, abspath
from gs_configurator import Configurator


APPLICATION_DIR = dirname(abspath(__file__))

resources_dir = f'{APPLICATION_DIR}/../../gs-share/resources'
config_file_name = 'gs-share.yaml'
config_file_dirs = '/etc/gs', '/opt/gs', APPLICATION_DIR, resources_dir

configuration = Configurator(config_file_name, config_file_dirs)
