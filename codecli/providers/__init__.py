# -*- coding: utf-8 -*-

import os
import re
from codecli.providers.base import KNOWN_PROVIDERS

_instance = None


class NoProviderFound(Exception):
    pass


def current_repo_git_url(remote):
    from codecli.utils import getoutput, is_under_git_repo

    if not is_under_git_repo(os.path.curdir):
        raise NoProviderFound("It is not under a git repo")

    for line in getoutput(['git', 'remote', '-v']).splitlines():
        words = line.split()
        if words[0] == remote and words[-1] == '(push)':
            giturl = words[1]
            break
    else:
        raise NoProviderFound("no remote %s found" % remote)
    return re.sub(r"(?<=http://).+:.+@", "", giturl)


def get_git_service_provider(force_provider=None):
    global _instance

    if force_provider is not None:
        def chooser(url):
            return force_provider in url
    else:
        def chooser(url):
            return url in current_repo_git_url('origin')

    if _instance is None:
        for url, sub_class in KNOWN_PROVIDERS.items():
            if chooser(url):
                _instance = sub_class()
                break
        else:
            raise TypeError("Not supported git provider")
    return _instance
