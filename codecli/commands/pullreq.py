from commands import getoutput
import webbrowser

from codecli.utils import print_log
import codecli.commands.fetch
from codecli.utils import get_current_branch_name, merge_with_base, \
    check_call, get_base_branch


def populate_argument_parser(parser):
    parser.add_argument('pr_id', nargs='?',
                        help="fetch and switch to a specific pullreq "
                        "(default: submit a new pullreq)")
    parser.add_argument('-t', '--target', metavar='USER',
                        help="act on a user's fork")


def main(args):
    if args.target:
        codecli.commands.fetch.add_remote(args.target)

    target = args.target or 'upstream'

    if args.pr_id:
        return fetch_and_switch_to_pr(args.pr_id, target=target)
    else:
        return submit_new_pullreq(target=target)

def fetch_and_switch_to_pr(pr_id, target='upstream'):
    check_call(['git', 'fetch', target,
                '+refs/pull/{0}/head:refs/remotes/{1}/pr/{0}'.format(
                    pr_id, target),
               ])
    check_call(['git', 'checkout', '{0}/pr/{1}'.format(target, pr_id)])

def submit_new_pullreq(target='upstream'):
    branch = get_current_branch_name()
    if branch == 'master':
        print_log('Pull request should never be from master')
        return 1

    merge_with_base(branch, remote=target)
    push_to_my_fork(branch)
    send_pullreq(branch, target=target)


def push_to_my_fork(branch):
    check_call(['git', 'push', '--set-upstream', 'origin', branch])


def send_pullreq(branch, target='upstream'):
    base = get_base_branch(branch)
    repourl = get_remote_repo_url('origin')
    base_repo = get_remote_repo_name(target)
    url = '%s/newpull/new?head_ref=%s&base_ref=%s&base_repo=%s' % (
        repourl, branch, base, base_repo)
    print_log("goto " + url)
    webbrowser.open(url)


def get_remote_repo_url(remote):
    for line in getoutput("git remote -v").splitlines():
        words = line.split()
        if words[0] == remote and words[-1] == '(push)':
            giturl = words[1]
            break
    else:
        raise Exception("no remote %s found" % remote)

    assert giturl.startswith('http://code.dapps.douban.com/')
    assert giturl.endswith('.git')
    repourl = giturl[: -len('.git')]
    return repourl

def get_remote_repo_name(remote):
    repourl = get_remote_repo_url(remote)
    return repourl[len('http://code.dapps.douban.com/'):]
