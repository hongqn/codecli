# -*- coding: utf-8 -*-

import re
import json
from getpass import getuser

from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

import codecli.utils as utils
from codecli.providers.base import GitServiceProvider


class GitEinProvider(GitServiceProvider):
    # FIXME allow to customize domain in config
    URLS = ['git.ein.plus']

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):
        head_user, _ = head_repo.split("/")
        base_user, _ = base_repo.split("/")

        url = "https://git.ein.plus/%s/-/merge_requests/new?" % head_repo + urlencode(
            {
                'merge_request[source_branch]': head_ref,
                'merge_request[source_project]': head_user,
                'merge_request[target_branch]': base_ref,
                'merge_request[target_project]': base_user,
            }
        )

        utils.print_log("goto " + url)
        utils.browser_open(url)

    def get_remote_repo_name(self, remote):
        repourl = self.get_remote_repo_url(remote)
        _, _, reponame = repourl.partition('git.ein.plus/')
        if not reponame:
            _, _, reponame = repourl.partition('git.ein.plus:')
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

        assert re.match(r"^git@git.ein.plus:.+\.git$", giturl) or re.match(
            r"^https://git.ein.plus/.+\.git$", giturl
        ), ("This url do not look like a git.ein.plus repo url: %s" % giturl)
        repourl = giturl[: -len('.git')]
        return repourl

    def get_repo_git_url(self, repo_name, login_user=''):
        if '://' in repo_name:
            return repo_name

        return 'https://git.ein.plus/%s.git' % repo_name

    def search_username(self):
        email = utils.get_user_email()
        payload = json.load(
            urlopen("https://api.git.ein.plus/search/users?" + urlencode(dict(q=email)))
        )
        return payload['items'][0]['login'] if payload['total_count'] else ''

    def get_username(self):
        return utils.get_config('user.name') or utils.get_user_name()

    def merge_config(self):
        email = utils.get_config('user.email')
        if not email:
            email = utils.getoutput(['git', 'config', 'user.email']).strip()
            if not email.endswith('@ein.plus'):
                email = '%s@ein.plus' % getuser()
            email = utils.ask(
                "Please enter your @ein.plus email [%s]: " % email, default=email
            )
            utils.set_config('user.email', email)

        name = utils.get_user_name()
        if not name:
            name = email.split('@')[0]
            name = utils.ask("Please enter your name [%s]: " % name, default=name)
            utils.set_config('user.name', name)

        for key, value in utils.iter_config():
            utils.check_call(['git', 'config', key, value])
