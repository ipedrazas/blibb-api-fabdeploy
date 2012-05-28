import os

from fabdeploy.api import DefaultConf


DIRNAME = os.path.dirname(__file__)


class BaseConf(DefaultConf):
    server_name = 'api.blibb.co'
    server_admin = 'blibb@blibb.com'

    repo_origin = 'https://vmihailenco@github.com/vmihailenco/blibb-api.git'

    supervisor_programs = ['gunicorn', 'redis_db', 'zmq_worker']

    django_dir = 'API'
    gunicorn_app = 'API:app'

    redis_path = '%(var_path)s/redis'
    redis_db_port = 6379


class StagingConf(BaseConf):
    sudo_user = 'fabdeploy'
    address = 'blibb_api@176.31.103.197'


class ProdConf(BaseConf):
    sudo_user = 'fabdeploy'
    address = 'blibb_api@176.31.103.197'


class LocalhostConf(BaseConf):
    address = 'blibb_api@localhost'
    sudo_user = 'vmihailenco'
