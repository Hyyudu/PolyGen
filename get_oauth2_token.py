'''
    This script will attempt to open your webbrowser,
    perform OAuth 2 authentication and print your access token.

    It depends on two libraries: oauth2client and gflags.

    To install dependencies from PyPI:

    $ pip install python-gflags oauth2client

    Then run this script:

    $ python get_oauth2_token.py
    
    This is a combination of snippets from:
    https://developers.google.com/api-client-library/python/guide/aaa_oauth
'''

refresh_token = '1/qWH0W58yRQzlnsUc4mhsWaaa34_3AwoRJTWZXAPgrAQ'

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow, argparser
from oauth2client.file import Storage

CLIENT_ID = '374210870301-m04qrnv2824ur59l07at476lg99qgsbl.apps.googleusercontent.com'
CLIENT_SECRET = 'm1K6cykbP-bWDt0Q7RrCppIi'


flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                           redirect_uri='http://example.com/auth_return')

storage = Storage('creds.data')

flags = argparser.parse_args(args=[])
credentials = run_flow(flow, storage, flags)

print("access_token: %s" % credentials.access_token)