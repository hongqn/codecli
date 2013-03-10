from __future__ import absolute_import

import os
from commands import getoutput
from subprocess import check_call as _check_call
from contextlib import contextmanager

GREEN = '\x1b[1;32m'
RESET = '\x1b[0m'


def get_current_branch_name():
    output = getoutput('git symbolic-ref HEAD')
    assert output.startswith('refs/heads/')
    return output[len('refs/heads/'):]


def get_base_branch(branch):
    if branch.startswith('hotfix-'):
        return branch.split('-')[1]
    return 'master'

def merge_with_base(branch, rebase=False):
    base = get_base_branch(branch)
    check_call(['git', 'fetch', 'upstream'])
    check_call(['git', 'rebase' if rebase else 'merge', 'upstream/%s' % base])


def set_track_upstream_pullrequest_branch():
    command = ('git config --add remote.upstream.fetch '
               '+refs/pull/*/head:refs/remotes/upstream/pr/*')
    check_call(command.split())


def check_call(cmd, *args, **kwargs):
    cmdstr = cmd if isinstance(cmd, basestring) else ' '.join(cmd)
    print_log(cmdstr)
    return _check_call(cmd, *args, **kwargs)


def print_log(outstr):
    print GREEN + ">> " + outstr + RESET


def repo_git_url(repo_name):
    return 'http://code.dapps.douban.com/%s.git' % repo_name


@contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield cwd
    finally:
        os.chdir(cwd)
