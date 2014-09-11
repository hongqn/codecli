# -*- coding: utf-8 -*-

import os
import glob
import importlib

KNOWN_PROVIDERS = {}


class ProviderMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ProviderMeta, cls).__new__
        new_class = super_new(cls, name, bases, attrs)
        for url in new_class.URLS:
            KNOWN_PROVIDERS[url] = new_class
        return new_class


class GitServiceProvider(object):
    URLS = []

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):
        raise NotImplementedError

    def get_remote_repo_name(self, remote):
        raise NotImplementedError

    def get_remote_repo_url(self, remote):
        raise NotImplementedError

GitServiceProvider = ProviderMeta(
    'GitServiceProvider', (GitServiceProvider,), {})


providers = glob.glob(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "provider_*.py"))

for each in providers:
    import_path = ".." + os.path.basename(each)[:-len('.py')]
    importlib.import_module(import_path, __name__)
