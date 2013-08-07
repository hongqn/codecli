from codecli.utils import check_call, get_branches, input
from codecli.commands.end import end_branch


def populate_argument_parser(parser):
    parser.add_argument('feature')


def main(args):
    branch = args.feature
    start(branch)


def start(branch, remote='upstream', fetch_args=[], base_ref='upstream/master'):
    existing_branches = get_branches()
    if branch in existing_branches:
        answer = input("Branch %s exists, (s)witch to it or re(c)reate "
                       "it?  (S/c) " % branch, pattern=r'[sScC]',
                       default='s')
        answer = answer.lower()[0]

        if answer == 's':
            check_call(['git', 'checkout', branch])
            return

        elif answer == 'c':
            end_branch(branch, force=True)

    check_call(['git', 'fetch', remote] + fetch_args)
    check_call(['git', 'checkout', '-b', branch, '--no-track', base_ref])
