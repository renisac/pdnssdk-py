import logging
import requests
import json
from pprint import pprint
from .exceptions import AuthError, TimeoutError
from prettytable import PrettyTable
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import os

from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

REMOTE_ADDR = os.environ.get('PDNS_REMOTE', 'https://pdns.ren-isac.net')
TOKEN = os.environ.get('PDNS_TOKEN')
SEARCH_LIMIT = os.environ.get('PDNS_SEARCH_LIMIT', 500)
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s][%(threadName)s] - %(message)s'
LOGLEVEL = 'INFO'

logger = logging.getLogger()


class Client(object):

    def __init__(self, remote=REMOTE_ADDR, token='', proxy=None, timeout=300, verify_ssl=True):

        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.token = token
        self.remote = remote

        self.session = requests.Session()
        self.session.headers["Accept"] = 'application/vnd.pdns.v0+json'
        self.session.headers['User-Agent'] = 'ri-pdnssdk-py/{}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token={}'.format(self.token)
        self.session.headers['Content-Type'] = 'application/json'

        if not self.verify_ssl:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def _get(self, uri, params={}):
        if not uri.startswith('http'):
            uri = self.remote + uri

        body = self.session.get(uri, params=params, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            logger.debug(err)

            if body.status_code == 401:
                raise AuthError('invalid token')
            elif body.status_code == 404:
                err = 'not found'
                raise RuntimeError(err)
            elif body.status_code == 408:
                raise TimeoutError('timeout')
            else:
                try:
                    err = json.loads(body.content).get('message')
                    raise RuntimeError(err)
                except ValueError as e:
                    err = body.content
                    logger.error(err)
                    raise RuntimeError(err)

        return json.loads(body.content)

    def search(self, q, limit=SEARCH_LIMIT):
        rv = self._get('/search', params={'q': q, 'limit': limit})
        return rv['data']


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ pdns -q 93.184.216.34 -d
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='pdns',
    )
    p.add_argument('--token', help='specify api token', default=TOKEN)
    p.add_argument('--remote', help='specify API remote [default %(default)s]', default=REMOTE_ADDR)
    p.add_argument('-q', '--search', help="search")
    p.add_argument('--limit', help='limit results [default %(default)s]', default=SEARCH_LIMIT)
    p.add_argument('--no-verify-ssl', action='store_true')
    p.add_argument('-d', '--debug', action="store_true")

    args = p.parse_args()

    verify_ssl = True
    if args.no_verify_ssl:
        verify_ssl = False

    cli = Client(args.remote, args.token, verify_ssl=verify_ssl)

    loglevel = logging.getLevelName(LOGLEVEL)

    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    logger.info("searching for {0}".format(args.search))
    try:
        rv = cli.search(args.search, limit=args.limit)
    except RuntimeError as e:
        import traceback
        traceback.print_exc()
        logger.error(e)
    except AuthError as e:
        logger.error('unauthorized')
    else:
        cols = ['query', 'type', 'answer', 'count', 'ttl', 'first', 'last', 'updated_at']
        t = PrettyTable(cols)

        for d in rv:
            r = []
            for c in cols:
                r.append(d.get(c))

            t.add_row(r)
            
        print(t.get_string(sortby='last'))


if __name__ == "__main__":
    main()
