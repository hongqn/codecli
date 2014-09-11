# -*- coding: utf-8 -*-

import re
from codecli.providers.base import KNOWN_PROVIDERS

_instance = None


def get_remote_repo_git_url(remote):
    from codecli.utils import getoutput
    for line in getoutput(['git', 'remote', '-v']).splitlines():
        words = line.split()
        if words[0] == remote and words[-1] == '(push)':
            giturl = words[1]
            break
    else:
        raise Exception("no remote %s found" % remote)
    return re.sub(r"(?<=http://).+:.+@", "", giturl)


def get_git_service_provider():
    global _instance
    if _instance is None:
        for url, sub_class in KNOWN_PROVIDERS.iteritems():
            giturl = get_remote_repo_git_url('origin')
            if url in giturl:
                _instance = sub_class()
                break
        else:
            raise TypeError("Not supported git provider")
    return _instance
