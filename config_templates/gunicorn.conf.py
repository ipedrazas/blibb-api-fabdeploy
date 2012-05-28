import multiprocessing


bind = '{{ gunicorn_bind }}'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 60
