from commands import getoutput
import webbrowser

from codecli.utils import get_current_branch_name, merge_with_base, \
        check_call, get_base_branch

def populate_argument_parser(parser):
    pass


def main(args):
    branch = get_current_branch_name()
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
    repo = giturl.split('/')[-1][:-4]
    url = 'http://code.dapps.douban.com/%s/newpull/new?head_ref=%s&base_ref=%s' \
            % (repo, branch, base)
    webbrowser.open(url)
