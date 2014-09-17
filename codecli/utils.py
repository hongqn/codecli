from __future__ import absolute_import

import os
import sys
import re
from subprocess import check_call as _check_call, call as _call, Popen, PIPE
from contextlib import contextmanager
import webbrowser


def get_current_branch_name():
    output = getoutput(['git', 'symbolic-ref', 'HEAD'])
    assert output.startswith('refs/heads/')
    return output[len('refs/heads/'):]


def remote_and_pr_id_from_pr_branch(branch):
    assert branch.startswith('pr/')
    words = branch.split('/', 2)
    if len(words) == 2:
        remote, pr_id = 'upstream', words[1]
    else:
        remote, pr_id = words[1], words[2]
    return remote, pr_id


def get_base_branch(branch, remote='upstream', remote_branch=None):
    if branch.startswith('hotfix-'):
        base_branch = branch.split('-')[1]
        return remote, [], base_branch

    if branch.startswith('pr/'):
        remote, pr_id = remote_and_pr_id_from_pr_branch(branch)
        ref = 'pr/{1}'.format(remote, pr_id)
        fetch_args = ['+refs/pull/{0}/head:refs/remotes/{1}/{2}'.format(
            pr_id, remote, ref)]
        return remote, fetch_args, ref

    return remote, [], remote_branch or 'master'


def merge_with_base(branch, rebase=False, remote='upstream',
                    remote_branch=None):
    remote, fetch_args, baseref = get_base_branch(branch, remote=remote,
                                                  remote_branch=remote_branch)
    check_call(['git', 'fetch', remote] + fetch_args)
    check_call(['git', 'rebase' if rebase else 'merge',
                '%s/%s' % (remote, baseref)])


def check_call(cmd, *args, **kwargs):
    cmdstr = cmd if isinstance(cmd, basestring) else ' '.join(cmd)
    print_log(cmdstr)
    return _check_call(cmd, *args, **kwargs)


def call(cmd, *args, **kwargs):
    cmdstr = cmd if isinstance(cmd, basestring) else ' '.join(cmd)
    print_log(cmdstr)
    return _call(cmd, *args, **kwargs)


def print_log(outstr):
    print >>sys.stderr, green(outstr)


def log_error(msg):
    print >>sys.stderr, red(msg)


def repo_git_url(repo_name, login_user='', provider=None):
    from codecli.providers import get_git_service_provider
    return get_git_service_provider(force_provider=provider).\
        get_repo_git_url(repo_name, login_user)


@contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield cwd
    finally:
        os.chdir(cwd)


def input(prompt, pattern=r'.*', default=''):
    while True:
        answer = raw_input(green(prompt))

        if not answer and default:
            return default

        if re.match(pattern, answer):
            return answer


def get_config_path():
    return os.path.expanduser('~/.codecli.conf')


def get_config(key):
    return getoutput(['git', 'config', '-f', get_config_path(), key]).strip()


def set_config(key, value):
    check_call(['git', 'config', '-f', get_config_path(), key, value])


def del_config(key):
    check_call(['git', 'config', '-f', get_config_path(), '--unset', key])


def iter_config():
    for line in getoutput(['git', 'config', '-f', get_config_path(),
                           '--list']).splitlines():
        line = line.strip()
        if not line:
            continue

        key, value = line.split('=', 1)
        yield key, value


def merge_config():
    """merge all config in ~/.codecli.conf to current git repo's config.

    Will prompt for email and name if they do not exist in ~/.codecli.conf.

    """
    from codecli.providers import get_git_service_provider
    return get_git_service_provider().merge_config()


def get_user_name():
    name = get_config('user.name')
    if not name:
        name = getoutput(['git', 'config', 'user.name']).strip()
    return name


def get_user_email():
    name = get_config('user.email')
    if not name:
        name = getoutput(['git', 'config', 'user.email']).strip()
    return name


def get_code_username():
    user_name = get_config('user.name')
    if not user_name:
        from codecli.providers import get_git_service_provider, NoProviderFound
        try:
            user_name = get_git_service_provider().get_username()
        except NoProviderFound:
            return None
    return user_name


def getoutput(cmd, **kwargs):
    stdout, stderr = Popen(cmd, stdout=PIPE, stderr=open(os.devnull, 'w'),
                           **kwargs).communicate()
    return stdout[:-1] if stdout[-1:] == '\n' else stdout


def get_branches(include_remotes=False):
    cmd = ['git', 'branch']
    if include_remotes:
        cmd += ['--all']

    return [x[2:].split()[0] for x in getoutput(cmd).splitlines()]


def get_remote_repo_url(remote):
    from codecli.providers import get_git_service_provider
    return get_git_service_provider().get_remote_repo_url(remote)


def get_remote_repo_name(remote):
    from codecli.providers import get_git_service_provider
    return get_git_service_provider().get_remote_repo_name(remote)


def send_pullreq(head_repo, head_ref, base_repo, base_ref):
    from codecli.providers import get_git_service_provider
    return get_git_service_provider().send_pullreq(
        head_repo, head_ref, base_repo, base_ref)


def browser_open(url):
    browser_name = get_config('webbrowser.name')
    if browser_name.lower() == 'none':
        return

    try:
        browser = webbrowser.get(browser_name or None)
    except webbrowser.Error:
        if browser_name:
            check_call([browser_name, url])
    else:
        browser.open(url)


def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')


def is_under_git_repo(path=None):
    """ Check if the given path is under a git repo
    """
    return getoutput(['git', 'rev-parse', '--is-inside-work-tree'], cwd=path) == 'true'
