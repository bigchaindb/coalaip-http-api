import os
from collections import namedtuple

BigchainDBConfiguration = namedtuple('BigchainDBConfiguration', [
    'hostname',
    'port',
    'api_path'
])


# Double check in case the environment variable is sent via Docker,
# which will send empty strings for missing environment variables
BDB_HOST = os.environ.get('BDB_NODE_HOST', None)
if not BDB_HOST:
    BDB_HOST = 'localhost'

BDB_PORT = os.environ.get('BDB_NODE_PORT', None)
if not BDB_PORT:
    BDB_PORT = '9984'

BDB_API_PATH = os.environ.get('BDB_NODE_API_PATH', None)
if not BDB_API_PATH:
    BDB_API_PATH = 'api/v1'


def get_bigchaindb_configuration():
    return BigchainDBConfiguration(BDB_HOST, BDB_PORT, BDB_API_PATH)


def get_bigchaindb_api_url():
    hostname, port, api_path = get_bigchaindb_configuration()
    return 'http://{hostname}:{port}/{api_path}'.format(hostname=hostname,
                                                        port=port,
                                                        api_path=api_path)
