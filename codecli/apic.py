"""Code API client"""

import json

from six.moves.urllib.request import urlopen

ENDPOINT = 'http://code.dapps.douban.com/api/'


def get(path):
    f = urlopen('http://code.dapps.douban.com/api/' + path)
    return json.load(f)


def get_pullinfo(repo, pr_id):
    return get('{0}/pull/{1}'.format(repo, pr_id))
