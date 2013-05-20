import webbrowser
import urllib

from codecli.utils import print_log
import codecli.commands.fetch
from codecli.commands.start import start
from codecli.utils import get_current_branch_name, merge_with_base, \
        check_call, get_base_branch, get_remote_repo_name, get_remote_repo_url, \
        remote_and_pr_id_from_pr_branch
from codecli.apic import get_pullinfo


def populate_argument_parser(parser):
    parser.add_argument('pr_id', nargs='?',
                        help="fetch and switch to a specific pullreq "
                        "(default: submit a new pullreq)")
    parser.add_argument('-t', '--target', metavar='USER',
                        help="act on a user's fork, or use the format of "
                        "USER:BRANCH to specify the target branch name")
    parser.add_argument('-n', '--nomerge', action='store_true',
                        help="submit pullreq without merge with upstream")


def main(args):
    if args.target:
        remote, remote_branch = get_remote_and_remote_branch_from_target(args.target)
        codecli.commands.fetch.add_remote(remote)
    else:
        remote, remote_branch = 'upstream', None

    if args.pr_id:
        return fetch_and_switch_to_pr(args.pr_id, remote=remote)
    else:
        return submit_new_pullreq(remote=remote, remote_branch=remote_branch,
                                  no_merge=args.nomerge)


def fetch_and_switch_to_pr(pr_id, remote='upstream'):
    ref = '{0}/pr/{1}'.format(remote, pr_id)
    branch = 'pr/{0}'.format(pr_id) if remote == 'upstream' \
            else 'pr/{0}/{1}'.format(remote, pr_id)
    fetch_args=['+refs/pull/{0}/head:refs/remotes/{1}'.format(pr_id, ref)]
    start(branch, remote=remote, fetch_args=fetch_args, base_ref=ref)


def get_remote_and_remote_branch_from_target(target):
    segs = target.split(':')
    remote = segs[0]
    remote_branch = segs[1] if len(segs) >= 2 else None
    return remote, remote_branch


def submit_new_pullreq(remote='upstream', remote_branch=None, no_merge=False):
    branch = get_current_branch_name()
    if branch == 'master':
        print_log('Pull request should never be from master')
        return 1

    if not no_merge:
        merge_with_base(branch, remote=remote, remote_branch=remote_branch)
    push_to_my_fork(branch)
    send_pullreq(branch, remote=remote, remote_branch=remote_branch)


def push_to_my_fork(branch):
    check_call(['git', 'push', '--set-upstream', 'origin', branch])


def send_pullreq(branch, remote='upstream', remote_branch=None):
    repourl = get_remote_repo_url('origin')
    remote, fetch_args, baseref = get_base_branch(branch, remote=remote,
                                                  remote_branch=remote_branch)
    base_repo = get_remote_repo_name(remote)

    if branch.startswith('pr/'):
        # for pr-on-pr
        remote, pr_id = remote_and_pr_id_from_pr_branch(branch)
        info = get_pullinfo(get_remote_repo_name(remote), pr_id)
        base_repo = info['head']['repo']['name']
        baseref = info['head']['ref']

    url = ('%s/newpull/new?' % repourl) + urllib.urlencode(dict(
        head_ref=branch, base_ref=baseref, base_repo=base_repo))
    print_log("goto " + url)
    webbrowser.open(url)


