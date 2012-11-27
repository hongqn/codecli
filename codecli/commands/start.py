from codecli.utils import check_call

def populate_argument_parser(parser):
    parser.add_argument('feature')


def main(args):
    branch = args.branch

    check_call('git checkout master', shell=True)
    check_call('git pull upstream master', shell=True)
    check_call('git checkout -b %s' % branch, shell=True)
