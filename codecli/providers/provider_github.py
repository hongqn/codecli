# -*- coding: utf-8 -*-

import re

from codecli.utils import print_log, browser_open, getoutput
from codecli.providers.base import GitServiceProvider


class GithubProvider(GitServiceProvider):
    URLS = ['github.com']

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):
        head_user, _ = head_repo.split("/")
        base_user, _ = base_repo.split("/")

        url = "https://github.com/%s/compare/%s:%s...%s:%s?expand=1" % (
            head_repo, base_user, base_ref, head_user, head_ref)

        print_log("goto " + url)
        browser_open(url)

    def get_remote_repo_name(self, remote):
        repourl = self.get_remote_repo_url(remote)
        _, _, reponame = repourl.partition('github.com:')
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

        assert re.match(r"^git@github.com:.+\.git$", giturl), \
            "This url do not look like a github repo url: %s" % giturl
        repourl = giturl[: -len('.git')]
        return repourl
