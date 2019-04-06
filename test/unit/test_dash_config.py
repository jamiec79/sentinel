import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from genix_config import GenixConfig


@pytest.fixture
def genix_conf(**kwargs):
    defaults = {
        'rpcuser': 'genixrpc',
        'rpcpassword': 'uCeiVie2Yoh3seesoovi',
        'rpcport': 4455,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    genix_config = genix_conf()
    creds = GenixConfig.get_rpc_creds(genix_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'genixrpc'
    assert creds.get('password') == 'uCeiVie2Yoh3seesoovi'
    assert creds.get('port') == 29241

    genix_config = genix_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = GenixConfig.get_rpc_creds(genix_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'genixrpc'
    assert creds.get('password') == 'uCeiVie2Yoh3seesoovi'
    assert creds.get('port') == 4455

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', genix_conf(), re.M)
    creds = GenixConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'genixrpc'
    assert creds.get('password') == 'uCeiVie2Yoh3seesoovi'
    assert creds.get('port') == 4455


def test_slurp_config_file():
    import tempfile

    genix_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    expected_stripped_config = """server=1
printtoconsole=1
txindex=1 # enable transaction index
"""

    with tempfile.NamedTemporaryFile(mode='w') as temp:
        temp.write(genix_config)
        temp.flush()
        conf = GenixConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
