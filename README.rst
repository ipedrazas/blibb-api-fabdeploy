Preparations
============

Create virtualenv::

    virtualenv env
    . env/bin/activate

Install django-fabdeploy-plus::

    pip install -r requirements.txt

Create ``fabdeploy`` user on target host::

    fab fabd.default_conf:address=user@host,sudo_user=user fabd.create_user

For example, to create ``fabdeploy`` user on ivan@getoi.com you have to use (where ivan is the user with sudo access):

    fab fabd.default_conf:address=ivan@oioi.me,sudo_user=ivan fabd.create_user

Create user for the project:

    fab fabd.conf:prod user_create

Install needed software::

    fab fabd.conf:prod install

Setup configs with::

    fab fabd.conf:prod setup

Deploy code::

    fab fabd.conf:deploy

Inspect available configs in ``fabconf.py``.
