from codecli.utils import check_call


def populate_argument_parser(parser):
    parser.add_argument('feature')


def main(args):
    branch = args.feature
    end_branch(branch)

def end_branch(branch):
    check_call(['git', 'branch', '-d', branch])
    check_call(['git', 'push', 'origin', ':%s' % branch])
