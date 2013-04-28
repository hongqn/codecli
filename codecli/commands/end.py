from codecli.utils import check_call, get_branches


def populate_argument_parser(parser):
    parser.add_argument('feature')


def main(args):
    branch = args.feature
    end_branch(branch)

def end_branch(branch):
    check_call(['git', 'branch', '-d', branch])
    if does_branch_exist_on_origin(branch):
        check_call(['git', 'push', 'origin', ':%s' % branch])

def does_branch_exist_on_origin(branch):
    branches = get_branches(include_remotes=True)
    return 'remotes/origin/{0}'.format(branch) in branches
