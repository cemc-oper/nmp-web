"""
config.py

use environment var
"""
import os
import yaml


class Config(object):
    def __init__(self, config_path):
        with open(config_path) as config_file:
            config_dict = yaml.load(config_file)
            nwpc_monitor_web_config = config_dict['nwpc_monitor_web']
            self.NWPC_MONITOR_WEB_CONFIG = nwpc_monitor_web_config

            if 'secret' in nwpc_monitor_web_config:
                secret_config = nwpc_monitor_web_config['secret']
                if 'key' in secret_config:
                    self.SECRET_KEY = secret_config['key']

            if 'debug' in nwpc_monitor_web_config:
                debug_config = nwpc_monitor_web_config['debug']
                if 'flask_debug' in debug_config:
                    flask_debug = debug_config['flask_debug']
                    if flask_debug is True:
                        self.DEBUG = True
                    elif flask_debug is not True:
                        self.DEBUG = False

            if 'mysql' in nwpc_monitor_web_config:
                mysql_config = nwpc_monitor_web_config['mysql']

                mysql_host = mysql_config['host']
                mysql_ip = mysql_host['ip']
                mysql_port = mysql_host['port']
                mysql_user = mysql_config['user']
                mysql_password = mysql_config['password']
                mysql_database = mysql_config['database']
                mysql_charset = mysql_config['charset']

                pool_recycle = mysql_config['pool_recycle']

                self.SQLALCHEMY_DATABASE_URI = \
                    "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
                        user=mysql_user,
                        password=mysql_password,
                        host=mysql_ip,
                        port=mysql_port,
                        database=mysql_database,
                        charset=mysql_charset
                    )

                self.SQLALCHEMY_POOL_RECYCLE = pool_recycle


def load_config():
    config_file_name = "production.config.yaml"
    if 'MODE' in os.environ:
        mode = os.environ['MODE']
        if mode == 'production':
            config_file_name = "production.config.yaml"
        elif mode == 'develop':
            config_file_name = "develop.config.yaml"
        else:
            config_file_name = mode + ".config.yaml"

    config_file_directory = os.path.dirname(__file__) + "/conf"

    config_file_path = config_file_directory + "/" + config_file_name

    print("config file path:", config_file_path)

    config_object = Config(config_file_path)

    return config_object
