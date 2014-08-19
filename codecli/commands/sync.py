from codecli.utils import get_current_branch_name, merge_with_base


def populate_argument_parser(parser):
    parser.add_argument('-r', '--rebase', action='store_true',
                        help="rebase with upstream")
    parser.add_argument('-b', '--base', help="Branch to rebase on")


def main(args):
    branch = get_current_branch_name()
    merge_with_base(branch, rebase=args.rebase, remote_branch=args.base)
