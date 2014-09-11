# -*- coding: utf-8 -*-

import re
import urllib

from codecli.utils import print_log, browser_open, getoutput
from codecli.providers.base import GitServiceProvider


class CodeProvider(GitServiceProvider):
    URLS = ['code.dapps.douban.com', 'code.intra.douban.com']

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):

        url = (('http://code.dapps.douban.com/%s/newpull/new?' % head_repo) +
               urllib.urlencode(dict(head_ref=head_ref, base_ref=base_ref,
                                     base_repo=base_repo)))
        print_log("goto " + url)
        browser_open(url)

    def get_remote_repo_name(self, remote):
        repourl = self.get_remote_repo_url(remote)
        _, _, reponame = repourl.partition('code.dapps.douban.com/')
        if not reponame:
            _, _, reponame = repourl.partition('code.intra.douban.com:')
        if not reponame:
            _, _, reponame = repourl.partition('code.dapps.douban.com:')
        return reponame

    def get_remote_repo_url(self, remote):
        for line in getoutput(['git', 'remote', '-v']).splitlines():
            words = line.split()
            if words[0] == remote and words[-1] == '(push)':
                giturl = words[1]
                break
        else:
            raise Exception("no remote %s found" % remote)

        giturl = re.sub(r"(?<=http://).+:.+@", "", giturl)
        assert (re.match(r"^http://([a-zA-Z0-9]+@)?code.dapps.douban.com/.+\.git$", giturl) or
                re.match(r"^git@code.(intra|dapps).douban.com:.+\.git$", giturl)), \
            "This url do not look like code dapps git repo url: %s" % giturl
        repourl = giturl[: -len('.git')]
        return repourl

    def get_repo_git_url(self, repo_name, login_user=''):
        if '://' in repo_name:
            return repo_name

        if login_user:
            login_user = login_user + '@'
        CODE_ADDR = 'code.dapps.douban.com'
        return 'http://%s%s/%s.git' % (login_user, CODE_ADDR, repo_name)
