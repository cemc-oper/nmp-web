# coding: utf-8
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

            # if 'mysql' in nwpc_monitor_web_config:
            #     mysql_config = nwpc_monitor_web_config['mysql']
            #
            #     mysql_host = mysql_config['host']
            #     mysql_ip = mysql_host['ip']
            #     mysql_port = mysql_host['port']
            #     mysql_user = mysql_config['user']
            #     mysql_password = mysql_config['password']
            #     mysql_database = mysql_config['database']
            #     mysql_charset = mysql_config['charset']
            #
            #     pool_recycle = mysql_config['pool_recycle']
            #
            #     self.SQLALCHEMY_DATABASE_URI = \
            #         "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
            #             user=mysql_user,
            #             password=mysql_password,
            #             host=mysql_ip,
            #             port=mysql_port,
            #             database=mysql_database,
            #             charset=mysql_charset
            #         )
            #
            #     self.SQLALCHEMY_POOL_RECYCLE = pool_recycle


def load_config(config_file_path):
    if config_file_path is None:
        if 'NMP_WEB_CONFIG' in os.environ:
            config_file_path = os.environ['NMP_WEB_CONFIG']
        else:
            raise Exception('config file path or NMP_WEB_CONFIG must be set.')

    print("config file path:", config_file_path)

    config_object = Config(config_file_path)

    return config_object
