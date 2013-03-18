import os
from getpass import getuser

from codecli.utils import check_call, repo_git_url, cd


def populate_argument_parser(parser):
    username = os.environ.get('GIT_AUTHOR_NAME', getuser())
    parser.add_argument('upstream', help="name of upstream repo [e.g. dae]")
    parser.add_argument('origin', help="name of my fork [e.g. dae_hongqn]")
    parser.add_argument('dir', help="directory to clone")
    parser.add_argument('--username', default=username,
                        help="douban unified account name [default: %(default)s]")


def main(args):
    name = args.upstream
    check_call(['git', 'clone', repo_git_url(args.origin), args.dir])
    with cd(args.dir):
        check_call(['git', 'remote', 'add', 'upstream', repo_git_url(name)])
        check_call(['git', 'config', 'user.email',
                    '%s@douban.com' % args.username.lower()])
        check_call(['git', 'config', 'user.name', args.username])

