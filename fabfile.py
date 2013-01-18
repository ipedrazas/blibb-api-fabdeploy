from fabdeploy import monkey
monkey.patch_all()
from fabric.api import *
from fabdeploy.api import *
setup_fabdeploy()
from fabdeploy.utils import upload_config_template
import requests


@task
def user_create():
    users.create.run()
    ssh.push_key.run(pub_key_file='~/.ssh/id_rsa.pub')


@task
def redis_push_configs():
    for filename in ['redis_db.conf']:
        upload_config_template(filename)


@task
def zmq_install():
    system.package_install.run(packages='libtool autoconf automake uuid-dev')
    with cd('/tmp'):
        run('wget http://download.zeromq.org/zeromq-3.2.1-rc2.tar.gz')
        run('tar -xzf zeromq-3.2.1-rc2.tar.gz')
        with cd('zeromq-3.2.1'):
            run('./configure')
            run('make')
            sudo('make install')
            sudo('ldconfig')
        run('rm -rf zeromq-3.2.1')


@task
def mongo_install():
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    upload_config_template(
        '10gen.list',
        '/etc/apt/sources.list.d/10gen.list',
        use_sudo=True)
    system.package_update.run()
    system.package_install.run(packages='mongodb-10gen')


@task
def install():
    # fabd.mkdirs.run()

    # # system.setup_backports.run()

    # system.package_install.run(
    #     packages='build-essential python-dev python-software-properties git-core')
    # pip.install_pip.run()

    # zmq_install()
    # mongo_install()

    # # redis.add_ppa.run()
    # redis.install.run()
    # with settings(warn_only=True):
    #     redis.remove_init.run()
    #     redis.stop.run()

    # nginx.add_ppa.run()
    # nginx.install.run()

    for app in ['supervisor', 'gunicorn']:
        pip.install.run(app=app)


@task
def setup():
    fabd.mkdirs.run()

    gunicorn.push_nginx_config.run()
    nginx.reload.run()

    supervisor.push_init_config.run()
    supervisor.push_d_config.run()
    supervisor.start.run()

    # redis_push_configs()
    gunicorn.push_config.run()
    supervisor.push_configs.run()
    supervisor.update.run()


@task
def deploy():
    fabd.mkdirs.run()
    release.create.run()

    git.init.run()
    git.pull.run()

    virtualenv.create.run()
    virtualenv.pip_install_req.run()
    virtualenv.pip_install.run(app='gunicorn')
    virtualenv.make_relocatable.run()

    # run('mkdir %(release_path)s/logs' % env.conf)
    # run('chmod 0770 %(release_path)s/logs' % env.conf)

    release.activate.run()
    supervisor.stop.run()
    supervisor.start.run()
    gunicorn.reload_with_supervisor.run()
    # send oi to notify deployment
    push_oi()


def push_oi():
    url = "http://api.oioi.me/ois/50a3a80552d4df76b8000000/push"
    login_key = '529d51cf1e45fbc725d68be23892919d498e8ff3'
    print "curl -d login_key=" + login_key + " " + url
    req = requests.post(url, data={'login_key': login_key})
    print req.content

