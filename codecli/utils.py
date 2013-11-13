from __future__ import absolute_import

import os
import sys
import re
from subprocess import check_call as _check_call, call as _call, Popen, PIPE
from contextlib import contextmanager
from getpass import getuser
import urllib
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


def repo_git_url(repo_name):
    if '://' in repo_name:
        return repo_name

    CODE_URL = 'http://code.dapps.douban.com'
    return '%s/%s.git' % (CODE_URL, repo_name)


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
    email = get_config('user.email')
    if not email:
        email = getoutput(['git', 'config', 'user.email']).strip()
        if not email.endswith('@douban.com'):
            email = '%s@douban.com' % getuser()
        email = input("Please enter your @douban.com email [%s]: " % email,
                      default=email)
        set_config('user.email', email)

    name = get_user_name()
    if not name:
        name = email.split('@')[0]
        name = input("Please enter your name [%s]: " % name, default=name)
        set_config('user.name', name)

    for key, value in iter_config():
        check_call(['git', 'config', key, value])


def get_user_name():
    name = get_config('user.name')
    if not name:
        name = getoutput(['git', 'config', 'user.name']).strip()
    return name


def get_code_username():
    email = get_config('user.email')
    return email.split('@')[0] if email else None


def getoutput(cmd):
    stdout, stderr = Popen(cmd, stdout=PIPE).communicate()
    return stdout[:-1] if stdout[-1:] == '\n' else stdout


def get_branches(include_remotes=False):
    cmd = ['git', 'branch']
    if include_remotes:
        cmd += ['--all']

    return [x[2:].split()[0] for x in getoutput(cmd).splitlines()]


def get_remote_repo_url(remote):
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


def get_remote_repo_name(remote):
    repourl = get_remote_repo_url(remote)
    _, _, reponame = repourl.partition('code.dapps.douban.com/')
    if not reponame:
        _, _, reponame = repourl.partition('code.intra.douban.com:')
    if not reponame:
        _, _, reponame = repourl.partition('code.dapps.douban.com:')
    return reponame


def send_pullreq(head_repo, head_ref, base_repo, base_ref):
    url = (('http://code.dapps.douban.com/%s/newpull/new?' % head_repo) +
           urllib.urlencode(dict(head_ref=head_ref, base_ref=base_ref,
                                 base_repo=base_repo)))
    print_log("goto " + url)
    browser_open(url)


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
