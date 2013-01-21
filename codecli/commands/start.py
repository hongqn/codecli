from codecli.utils import check_call

def populate_argument_parser(parser):
    parser.add_argument('feature')


def main(args):
    branch = args.feature

    check_call(['git', 'fetch', 'upstream'])
    check_call(['git', 'checkout', '-b', branch, 'upstream/master'])
