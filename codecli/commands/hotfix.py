from codecli.utils import check_call

def populate_argument_parser(parser):
    parser.add_argument('start_point', default='release',
                        help="branch to start hotfix from [default: %(default)s]")
    parser.add_argument('issue', help="a short name for the hotfix")


def main(args):
    branch_name = 'hotfix-%s-%s' % (args.start_point, args.issue)
    check_call(['git', 'fetch', 'upstream'])
    check_call(['git', 'checkout', '-b', branch_name, 'upstream/'+args.start_point])
    check_call(['git', 'branch', '--set-upstream-to', 'origin/%s' % branch_name])
