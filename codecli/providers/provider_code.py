# -*- coding: utf-8 -*-

import re
from getpass import getuser
import json

from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

import codecli.utils as utils
from codecli.providers.base import GitServiceProvider


class CodeProvider(GitServiceProvider):
    URLS = ['code.dapps.douban.com', 'code.intra.douban.com']

    def send_pullreq(self, head_repo, head_ref, base_repo, base_ref):

        url = ('http://code.dapps.douban.com/%s/newpull/new?' % head_repo) + urlencode(
            dict(head_ref=head_ref, base_ref=base_ref, base_repo=base_repo)
        )
        utils.print_log("goto " + url)
        utils.browser_open(url)

    def get_remote_repo_name(self, remote):
        repourl = self.get_remote_repo_url(remote)
        _, _, reponame = repourl.partition('code.dapps.douban.com/')
        if not reponame:
            _, _, reponame = repourl.partition('code.intra.douban.com:')
        if not reponame:
            _, _, reponame = repourl.partition('code.dapps.douban.com:')
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
        assert re.match(
            r"^http://([a-zA-Z0-9]+@)?code.dapps.douban.com/.+\.git$", giturl
        ) or re.match(r"^git@code.(intra|dapps).douban.com:.+\.git$", giturl), (
            "This url do not look like code dapps git repo url: %s" % giturl
        )
        repourl = giturl[: -len('.git')]
        return repourl

    def get_repo_git_url(self, repo_name, login_user=''):
        if '://' in repo_name:
            return repo_name

        if login_user:
            login_user = login_user + '@'
        CODE_ADDR = 'code.dapps.douban.com'
        return 'http://%s%s/%s.git' % (login_user, CODE_ADDR, repo_name)

    def get_username(self):
        email = utils.get_config('user.email')
        return email.split('@')[0] if email and email.endswith('@douban.com') else None

    def merge_config(self):
        email = utils.get_config('user.email')
        if not email:
            email = utils.getoutput(['git', 'config', 'user.email']).strip()
            if not email.endswith('@douban.com'):
                email = '%s@douban.com' % getuser()
            email = utils.ask(
                "Please enter your @douban.com email [%s]: " % email, default=email
            )
            utils.set_config('user.email', email)

        name = utils.get_user_name()
        if not name:
            name = email.split('@')[0]
            name = utils.ask("Please enter your name [%s]: " % name, default=name)
            utils.set_config('user.name', name)

        for key, value in utils.iter_config():
            utils.check_call(['git', 'config', key, value])

    def get_pullinfo(self, repo, pr_id):
        url = 'http://code.dapps.douban.com/api/{0}/pull/{1}'.format(repo, pr_id)
        f = urlopen(url)
        data = json.load(f)
        return data['head']['repo']['name'], data['head']['ref']
