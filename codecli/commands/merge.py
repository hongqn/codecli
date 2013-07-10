from codecli.utils import check_call, send_pullreq, get_remote_repo_name, \
        get_branches, input


def populate_argument_parser(parser):
    parser.add_argument('from_branch', help="upstream branch name")
    parser.add_argument('to_branch', help="upstream branch name")
    parser.add_argument('--push', action='store_true',
                        help="push to upstream if successfully merged "
                             "[default: send pull request]")


def main(args):
    if args.push:
        return merge_and_push(args.from_branch, args.to_branch)

    else:
        return send_merge_pullreq(args.from_branch, args.to_branch)


def merge_and_push(from_branch, to_branch):
    check_call(['git', 'fetch', 'upstream'])
    local_branch = 'merge/{0}-to-{1}'.format(from_branch, to_branch)
    existing_branches = get_branches()
    answer = 'd'
    if local_branch in existing_branches:
        answer = input("Branch {0} exists.  Should I (d)estroy it and "
                       "re-merge from scratch, or re(u)se it in case you "
                       "were resolving merge conflicts just now? (D/u) "
                       .format(local_branch), pattern=r'[dDuU]',
                       default='d').lower()[0]

    if answer == 'd':
        check_call(['git', 'checkout',
                    '-B', local_branch, 'upstream/{0}'.format(to_branch)])

    else:
        check_call(['git', 'checkout', local_branch])

    check_call(['git', 'merge', 'upstream/{0}'.format(from_branch)])
    check_call(['git', 'push', 'upstream',
                '{0}:{1}'.format(local_branch, to_branch)])
    check_call(['git', 'checkout', 'master'])
    check_call(['git', 'branch', '-d', local_branch])


def send_merge_pullreq(from_branch, to_branch):
    repo = get_remote_repo_name('upstream')
    send_pullreq(repo, from_branch, repo, to_branch)
