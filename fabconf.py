import os

from fabdeploy.api import DefaultConf


DIRNAME = os.path.dirname(__file__)


class BaseConf(DefaultConf):
    
    server_admin = 'blibb@blibb.co'

    repo_origin = 'https://ipedrazas@github.com/ipedrazas/blibb-api.git'

    supervisor_programs = ['gunicorn', 'redis_db', 'zmq_worker']

    django_dir = 'API'
    gunicorn_app = 'API:app'

    redis_path = '%(var_path)s/redis'
    redis_db_port = 6379


class StagingConf(BaseConf):
    server_name = 'api.blibb.co'
    sudo_user = 'fabdeploy'
    address = 'blibb_api@blibb.co'


class ProdConf(BaseConf):
    server_name = 'api.blibb.it'
    sudo_user = 'fabdeploy'
    address = 'blibb_api@blibb.it'


class LocalhostConf(BaseConf):
    server_name = 'api.devblibb.com'
    address = 'blibb_api@localhost'
    sudo_user = 'ivan'

