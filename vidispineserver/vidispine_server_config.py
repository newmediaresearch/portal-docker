import yaml
server_config_file = '/etc/vidispine/server.yaml'
stream = open(server_config_file, 'r')
server_config = yaml.load(stream)


server_config['database'] = server_config.get('database', {})
server_config['database']['url'] = 'jdbc:postgresql://${POSTGRES_HOST}/${VIDISPINE_DB_NAME}'  # NOQA
server_config['database']['user'] = '${VIDISPINE_DB_USER}'
server_config['database']['password'] = '${VIDISPINE_DB_PSWD}'


with open(server_config_file, 'w') as yaml_file:
    yaml_file.write(yaml.dump(server_config, default_flow_style=False))
