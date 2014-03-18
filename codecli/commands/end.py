import subprocess

from codecli.utils import (check_call, get_branches, get_current_branch_name,
                           merge_with_base, log_error, input)


def populate_argument_parser(parser):
    parser.add_argument('branches', nargs='*', help="[default: current branch]")
    parser.add_argument('-f', '--force', action='store_true',
                        help="force branch deletion even if not "
                        "fully merged (git branch -D)")


def main(args):
    branches = args.branches
    if not branches:
        branches = [get_current_branch_name()]
    assert 'master' not in branches, "Cannot terminate master branch!"
    for br in branches:
        try:
            end_branch(br, args.force)
        except subprocess.CalledProcessError as e:
            print(e)
            log_error("Fail to delete branch %s." % br)


def end_branch(branch, force):
    if branch == get_current_branch_name():
        check_call(['git', 'checkout', 'master'])
    if force:
        check_call(['git', 'branch', '-D', branch])
    else:
        try:
            check_call(['git', 'branch', '-d', branch])
        except subprocess.CalledProcessError:
            log_error("Failed to delete branch %s because it is not fully "
                      "merged (may cause commits loss)." % branch)
            answer = input("Do you want to force to delete it even so? (y/N) ",
                           pattern=r'[nNyY].*', default='n')
            if answer[0] in 'yY':
                check_call(['git', 'branch', '-D', branch])
            else:
                raise

    if does_branch_exist_on_origin(branch):
        check_call(['git', 'push', 'origin', ':%s' % branch])


def does_branch_exist_on_origin(branch):
    branches = get_branches(include_remotes=True)
    return 'remotes/origin/{0}'.format(branch) in branches
