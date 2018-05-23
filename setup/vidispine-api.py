#!/usr/bin/env python

import os
import copy
import json
import urllib2
import sys
import traceback

from base64 import b64encode
from urllib import urlencode, quote_plus
from urlparse import urljoin
from optparse import OptionParser
from xml.dom.minidom import parseString
from pprint import pprint
from StringIO import StringIO

ALLOWED_DEBUG_PRINT = ('application/json', 'application/xml', 'text/plain')

HTTPError = urllib2.HTTPError

HTTP_PROXY = os.getenv('HTTP_PROXY', None)
if HTTP_PROXY:
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


DESCRIPTION = 'vidispine-add-storage'
USAGE = "usage:%prog [options] url"
parser = OptionParser(description=DESCRIPTION, usage=USAGE)


def parse_opts():
    parser.add_option(
        '-X',
        '--method',
        action='store',
        default='GET',
        dest='method',
        help='Method.  Defauts to GET',
    )
    parser.add_option(
        '-H',
        '--headers',
        action='store',
        default='{}',
        dest='headers',
        help='Headers.  Uses JSON-compatible dictionary',
    )
    parser.add_option(
        '-d',
        '--data',
        action='store',
        default=None,
        dest='data',
        help='JSON/XML data',
    )
    parser.add_option(
        '-a',
        '--accept',
        action='store',
        default='application/json',
        dest='header_accept',
        help='Accept Header',
    )
    parser.add_option(
        '-c',
        '--content-type',
        action='store',
        default='application/json',
        dest='header_contenttype',
        help='Content-Type Header',
    )
    parser.add_option(
        '-f',
        '--file',
        action='store',
        default=None,
        dest='file',
        help='File containing JSON/XML',
    )
    parser.add_option(
        '-b',
        '--base',
        action='store',
        default='API',
        dest='VIDISPINE_BASE',
        help='Base of URL, defaults to API',
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        dest='debug',
        default=False,
        help='Verbose logging',
    )
    parser.add_option(
        '-s',
        '--silent',
        action='store_true',
        dest='silent',
        default=False,
        help='No output.',
    )
    parser.add_option(
        '-n',
        '--disable-expandvars',
        action='store_true',
        dest='disable_expandvars',
        default=False,
        help='Disable File Environment Variables',
    )
    options, args = parser.parse_args()
    return (options, args)


class VidispineApi():
    def __init__(
        self,
        VIDISPINE_HOST='127.0.0.1',
        VIDISPINE_PASSWORD='admin',
        VIDISPINE_USERNAME='admin',
        VIDISPINE_PORT=8080,
        VIDISPINE_BASE='API',
        debug=False,
        runas=None,
    ):
        self.debug = os.getenv(
            'VIDISPINE_DEBUG',
            debug
        )
        self.VIDISPINE_HOST = os.getenv(
            'VIDISPINE_HOST',
            VIDISPINE_HOST,
        )
        self.VIDISPINE_PASSWORD = os.getenv(
            'VIDISPINE_PASSWORD',
            VIDISPINE_PASSWORD,
        )
        self.VIDISPINE_USERNAME = os.getenv(
            'VIDISPINE_USERNAME',
            VIDISPINE_USERNAME,
        )
        self.VIDISPINE_PORT = os.getenv(
            'VIDISPINE_PORT',
            VIDISPINE_PORT,
        )

        if self.VIDISPINE_HOST is None:
            raise ValueError('VIDISPINE_HOST is not set')
        if 'http://' not in self.VIDISPINE_HOST:
            self.VIDISPINE_HOST = 'http://{0}'.format(self.VIDISPINE_HOST)
        base = "{0}:{1}/".format(self.VIDISPINE_HOST, self.VIDISPINE_PORT)
        self.baseurl = urljoin(base, "{0}/".format(VIDISPINE_BASE))
        self.headers = {
            'content-type': 'application/json', 'accept': 'application/json'
        }
        self.auth = b64encode(
            '{0}:{1}'.format(self.VIDISPINE_USERNAME, self.VIDISPINE_PASSWORD)
        )
        self.headers['authorization'] = 'Basic {0}'.format(self.auth)
        if runas:
            self.headers.update({'runas': runas})

    def request(self, **kwargs):
        kwargs['auth'] = self.auth

        if 'headers' in kwargs:
            tmp_headers = copy.copy(self.headers)
            lower_headers = dict(
                (k.lower(), v) for k, v in kwargs['headers'].iteritems()
            )
            tmp_headers.update(lower_headers)
            kwargs['headers'] = tmp_headers
        else:
            kwargs['headers'] = self.headers

        if 'runas' in kwargs:
            kwargs['headers'].update({'RunAs': kwargs['runas']})

        if 'url' not in kwargs:
            raise ValueError("url is not set")
        if kwargs['url'].startswith('/'):
            kwargs['url'] = kwargs['url'][1:]

        if 'matrix_params' in kwargs:
            matrix_params = kwargs['matrix_params']
            matrix_list = []
            for matrix_param in matrix_params:
                for k, v in matrix_param.iteritems():
                    param = '{0}={1}'.format(k, v)
                    matrix_list.append(param)
            kwargs['url'] = kwargs['url'] + ';' + ';'.join(matrix_list)

        if 'query_params' in kwargs:
            # pop content-path as not urlencoded
            content_path = kwargs['query_params'].pop('p', None)
            jobmetadata = kwargs['query_params'].pop('jobmetadata', None)
            encoded_params = urlencode(kwargs['query_params'])
            if content_path:
                encoded_params = encoded_params + '&p=' + content_path
            if jobmetadata:
                if type(jobmetadata) is dict:
                    for k, v in jobmetadata.items():
                        jobmetadata_key = quote_plus('{0}='.format(k))
                        # Built-in job metadata bools are lowercase str
                        if type(v) is bool:
                            v = str(v).lower
                        jobmetadata_val = quote_plus(v)
                        encoded_params += '&jobmetadata=' + jobmetadata_key + jobmetadata_val  # noqa: E501
                else:
                    encoded_params += '&jobmetadata=' + jobmetadata
            kwargs['url'] = kwargs['url'] + '?' + encoded_params

        kwargs['url'] = urljoin(self.baseurl, kwargs['url'])

        if 'method' in kwargs:
            kwargs['method'] = kwargs['method'].upper()
        else:
            kwargs['method'] = 'GET'

        if 'data' in kwargs:
            if kwargs['headers']['content-type'] == 'application/json':
                kwargs['data'] = json.dumps(kwargs['data'])

        if self.debug:
            tmp_kwargs = copy.deepcopy(kwargs)
            tmp_kwargs.pop('auth')
            tmp_kwargs.get('headers').pop('authorization')
            if kwargs['headers']['content-type'] not in ALLOWED_DEBUG_PRINT:
                if kwargs.get('data'):
                    tmp_kwargs.pop('data')
                    print 'VidispineApi: Request {0}'.format(tmp_kwargs)
                    print 'VidispineApi: Ommiting data'
            else:
                print 'VidispineApi: Request {0}'.format(tmp_kwargs)

        request = urllib2.Request(
            url=kwargs['url'],
            headers=kwargs['headers'],
            data=kwargs.get('data', None)
        )
        request.get_method = lambda: kwargs['method']
        try:
            response = urllib2.urlopen(request)
        except HTTPError, e:
            error_body = e.readlines()
            if error_body:
                e.msg = error_body
            raise e
        try:
            response_content = response.read()
            if response_content:
                response_content_type = response.info().getheader(
                    'Content-Type'
                )
                if self.debug:
                    print 'VidispineApi: Response Code {0}'.format(
                        response.getcode()
                    )
                    print 'VidispineApi: Response Content-Type {0}'.format(
                        response_content_type
                    )
                    if response_content_type in ALLOWED_DEBUG_PRINT:
                        print 'VidispineApi: Response {0}'.format(
                            response_content
                        )
                if response.headers.get('content-type') == 'application/json':
                    return json.loads(response_content)
                return response_content
            elif response.getcode() == 200:
                return True
        except AttributeError:
            return response


if __name__ == '__main__':
    options, args = parse_opts()
    method = options.method
    debug = options.debug
    headers = {
        'content-type': options.header_contenttype,
        'accept': options.header_accept,
    }
    try:
        option_headers = json.loads(options.headers)
    except ValueError as e:
        print "ERROR: headers formatted incorrectly. See help."
        sys.exit(1)
    headers.update(option_headers)
    if headers.get('content-type', 'application/json') == 'application/json':
        is_json = True
    else:
        is_json = False
    if options.file:
        with open(options.file, 'r') as datafile:
            if is_json:
                try:
                    if options.disable_expandvars:
                        data = json.load(datafile)
                    else:
                        env_datafile = os.path.expandvars(datafile.read())
                        data = json.load(StringIO(env_datafile))
                except ValueError as e:
                    print "ERROR: unable to load JSON data"
                    sys.exit(1)
            else:
                data = datafile.read()
    else:
        data = options.data
        if is_json:
            if data is not None:
                try:
                    data = json.loads(options.data)
                except ValueError as e:
                    print "ERROR: unable to load JSON data"
                    sys.exit(1)
    if len(args) is not 1:
        print "ERROR: Wrong number of arguments for url"
        sys.exit(1)
    url = args[0]
    try:
        vs = VidispineApi(debug=debug, VIDISPINE_BASE=options.VIDISPINE_BASE)
        output = vs.request(
            url=url,
            method=method,
            headers=headers,
            data=data,
        )
        if options.silent:
            sys.exit(0)
        if headers.get('accept') == 'application/xml':
            xml = parseString(output)
            output_xml = xml.toprettyxml()
            sys.stdout.write(output_xml)
            sys.exit(0)
        if headers.get('accept') == 'text/plain':
            sys.stdout.write(output)
            sys.exit(0)
        pprint(output)
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e)
    except Exception:
        if options.silent:
            sys.exit(1)
        trace = traceback.format_exc()
        print trace
        raise
