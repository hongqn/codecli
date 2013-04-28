"""Code API client"""

import urllib
import json

ENDPOINT = 'http://code.dapps.douban.com/api/'

def get(path):
    f = urllib.urlopen('http://code.dapps.douban.com/api/' + path)
    return json.load(f)

def get_pullinfo(repo, pr_id):
    return get('{0}/pull/{1}'.format(repo, pr_id))
