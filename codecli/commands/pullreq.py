from commands import getoutput
from subprocess import check_call
import webbrowser

from codecli.utils import get_current_branch_name, merge_with_master

def populate_argument_parser(parser):
    pass


def main(args):
    branch = get_current_branch_name()
    merge_with_master(branch)
    push_to_my_fork(branch)
    send_pullreq(branch)


def push_to_my_fork(branch):
    check_call('git push origin %s' % branch, shell=True)


def send_pullreq(branch):
    giturl = getoutput("git remote -v | grep origin | grep push | awk '{ print $2 }'").strip()
    assert giturl.startswith('http://code.dapps.douban.com/')
    assert giturl.endswith('.git')
    repo = giturl.split('/')[-1][:-4]
    url = 'http://code.dapps.douban.com/%s/pull/new?head_ref=%s' % (repo, branch)
    webbrowser.open(url)
