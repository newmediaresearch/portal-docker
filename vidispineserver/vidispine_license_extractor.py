from ConfigParser import RawConfigParser

LICENSE_FILE = '/etc/vidispine/License.lic'
PORTAL_KEY = '/usr/local/bin/key'

config = RawConfigParser()
config.read(PORTAL_KEY)

with open(LICENSE_FILE, 'w') as outfile:
    for item in config.items('vidispine'):
        outfile.write('{}={}\n'.format(item[0], item[1]))
