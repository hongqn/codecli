from codecli.utils import get_current_branch_name, merge_with_base

def populate_argument_parser(parser):
    pass

def main(args):
    branch = get_current_branch_name()
    merge_with_base(branch)

