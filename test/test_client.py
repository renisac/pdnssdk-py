import py.test

from ri_pdnssdk.client import Client


def test_client_http():
    cli = Client('https://localhost:5000', '12345')
    assert cli.remote == 'https://localhost:5000'

    assert cli.token == '12345'
