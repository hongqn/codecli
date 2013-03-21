from __future__ import absolute_import

import os
from commands import getoutput
from subprocess import check_call as _check_call
from contextlib import contextmanager
from getpass import getuser

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

def merge_with_base(branch, rebase=False, remote='upstream'):
    base = get_base_branch(branch)
    check_call(['git', 'fetch', remote])
    check_call(['git', 'rebase' if rebase else 'merge',
                '%s/%s' % (remote, base)])


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


def input(prompt):
    return raw_input(GREEN + prompt + RESET)


def merge_config():
    """merge all config in ~/.codecli.conf to current git repo's config.

    Will prompt for email and name if they do not exist in ~/.codecli.conf.

    """
    path = os.path.expanduser('~/.codecli.conf')

    email = getoutput('git config -f "%s" user.email' % path).strip()
    if not email:
        email = getoutput('git config user.email').strip()
        if not email.endswith('@douban.com'):
            email = '%s@douban.com' % getuser()
        email = input("Please enter your @douban.com email [%s]: " % email
                     ) or email
        check_call(['git', 'config', '-f', path, 'user.email', email])

    name = getoutput('git config -f "%s" user.name' % path).strip()
    if not name:
        name = getoutput('git config user.name').strip()
        if not name:
            name = email.split('@')[0]
        name = input("Please enter your name [%s]: " % name) or name
        check_call(['git', 'config', '-f', path, 'user.name', name])

    for line in getoutput('git config -f "%s" --list' % path).splitlines():
        line = line.strip()
        if not line:
            continue

        key, value = line.split('=', 1)
        check_call(['git', 'config', key, value])
