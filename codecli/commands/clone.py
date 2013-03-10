import os
from getpass import getuser

from codecli.utils import check_call, repo_git_url, cd


def populate_argument_parser(parser):
    parser.add_argument('repo', help="name of repo [e.g. dae]")
    parser.add_argument('dir', nargs='?', help="directory to clone to")
    username = os.environ.get('GIT_AUTHOR_NAME', getuser())
    parser.add_argument('--username', default=username,
                        help="douban unified account name [default: %(default)s]")


def main(args):
    cmd =['git', 'clone', repo_git_url(args.repo)]
    if args.dir:
        cmd.append(args.dir)
        dir = args.dir
    else:
        dir = args.repo.split('/')[-1]
    check_call(cmd)

    with cd(dir):
        check_call(['git', 'config', 'user.email',
                    '%s@douban.com' % args.username.lower()])
        check_call(['git', 'config', 'user.name', args.username])

