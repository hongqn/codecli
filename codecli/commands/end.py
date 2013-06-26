from codecli.utils import (check_call, get_branches, get_current_branch_name,
                           merge_with_base)


def populate_argument_parser(parser):
    parser.add_argument('branch', nargs='?', help="[default: current branch]")


def main(args):
    branch = args.branch
    if not branch:
        branch = get_current_branch_name()
    assert branch != 'master', "Cannot terminate master branch!"
    end_branch(branch)

def end_branch(branch):
    merge_with_base(branch)
    check_call(['git', 'push', 'origin', branch])
    if branch == get_current_branch_name():
        check_call(['git', 'checkout', 'master'])
    check_call(['git', 'branch', '-d', branch])
    if does_branch_exist_on_origin(branch):
        check_call(['git', 'push', 'origin', ':%s' % branch])

def does_branch_exist_on_origin(branch):
    branches = get_branches(include_remotes=True)
    return 'remotes/origin/{0}'.format(branch) in branches
