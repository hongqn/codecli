# -*- coding: utf-8 -*-

import re
import json
import urllib

import codecli.utils as utils
from codecli.providers.base import GitServiceProvider


class GithubProvider(GitServiceProvider):
    URLS = ['github.com']

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):
        head_user, _ = head_repo.split("/")
        base_user, _ = base_repo.split("/")

        url = "https://github.com/%s/compare/%s:%s...%s:%s?expand=1" % (
            head_repo, base_user, base_ref, head_user, head_ref)

        utils.print_log("goto " + url)
        utils.browser_open(url)

    def get_remote_repo_name(self, remote):
        repourl = self.get_remote_repo_url(remote)
        _, _, reponame = repourl.partition('github.com/')
        if not reponame:
            _, _, reponame = repourl.partition('github.com:')
        return reponame

    def get_remote_repo_url(self, remote):
        for line in utils.getoutput(['git', 'remote', '-v']).splitlines():
            words = line.split()
            if words[0] == remote and words[-1] == '(push)':
                giturl = words[1]
                break
        else:
            raise Exception("no remote %s found" % remote)

        giturl = re.sub(r"(?<=http://).+:.+@", "", giturl)

        assert (re.match(r"^git@github.com:.+\.git$", giturl) or
                re.match(r"^https://github.com/.+\.git$", giturl)), \
            "This url do not look like a github repo url: %s" % giturl
        repourl = giturl[: -len('.git')]
        return repourl

    def get_repo_git_url(self, repo_name, login_user=''):
        if '://' in repo_name:
            return repo_name

        return 'https://github.com/%s.git' % repo_name

    def search_username(self):
        email = utils.get_user_email()
        payload = json.load(urllib.urlopen(
            "https://api.github.com/search/users?" +
            urllib.urlencode(dict(q=email))))
        return payload['items'][0]['login'] if payload['total_count'] else ''

    def get_username(self):
        return utils.get_config('user.name') or utils.get_user_name()

    def merge_config(self):
        user_name = utils.get_config('user.name')
        if not user_name:
            user_name = self.search_username()
            if user_name:
                utils.set_config('user.name', user_name)
