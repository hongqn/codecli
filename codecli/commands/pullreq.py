import sys
from commands import getoutput
from codecli.utils import print_log
import webbrowser

from codecli.utils import get_current_branch_name, merge_with_base, \
    check_call, get_base_branch


def populate_argument_parser(parser):
    pass


def main(args):
    branch = get_current_branch_name()
    if branch == 'master':
        print_log('Pull request should never be from master')
        sys.exit(1)
    merge_with_base(branch)
    push_to_my_fork(branch)
    send_pullreq(branch)


def push_to_my_fork(branch):
    check_call('git push --set-upstream origin %s' % branch, shell=True)


def send_pullreq(branch):
    base = get_base_branch(branch)
    giturl = getoutput("git remote -v | grep origin | grep push | awk '{ print $2 }'").strip()
    assert giturl.startswith('http://code.dapps.douban.com/')
    assert giturl.endswith('.git')
    repo = giturl[: -len('.git')]
    url = '%s/newpull/new?head_ref=%s&base_ref=%s' % (repo, branch, base)
    print_log("goto " + url)
    webbrowser.open(url)
