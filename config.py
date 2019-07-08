import os
DB_INFO = {
    'host': os.environ.get('host','host.docker.internal'),
    'user': os.environ.get('user','root'),
    'port': os.environ.get('port',3306),
    'passwd': os.environ.get('passwd'),
    'database': os.environ.get('database','article'),
    'charset': 'utf8',
}