import os
import yaml

SERVER_CONFIG_FILE = '/etc/vidispine/server.yaml'
stream = open(SERVER_CONFIG_FILE, 'r')
server_config = yaml.load(stream)

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
VIDISPINE_DB_NAME = os.getenv('VIDISPINE_DB_NAME')
VIDISPINE_DB_USER = os.getenv('VIDISPINE_DB_USER')
VIDISPINE_DB_PSWD = os.getenv('VIDISPINE_DB_PSWD')

server_config['database'] = server_config.get('database', {})
server_config['database']['url'] = 'jdbc:postgresql://{}/{}'.format(
    POSTGRES_HOST, VIDISPINE_DB_NAME
)

server_config['database']['user'] = VIDISPINE_DB_USER
server_config['database']['password'] = VIDISPINE_DB_PSWD


with open(SERVER_CONFIG_FILE, 'w') as yaml_file:
    yaml_file.write(yaml.dump(server_config, default_flow_style=False))
