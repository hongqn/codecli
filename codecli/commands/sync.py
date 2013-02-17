from codecli.utils import get_current_branch_name, merge_with_base


def populate_argument_parser(parser):
    parser.add_argument('-r', '--rebase', action='store_true',
                        help="rebase with upstream")


def main(args):
    branch = get_current_branch_name()
    merge_with_base(branch, rebase=args.rebase)
