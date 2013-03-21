from commands import getoutput
from codecli.utils import check_call, repo_git_url


def populate_argument_parser(parser):
    parser.add_argument('username',
                        help="username of another fork of this repo")


def main(args):
    add_remote(args.username)
    fetch(args.username)


def add_remote(username):
    output = getoutput('git remote -v')
    for line in output.splitlines():
        words = line.split()
        if words[0] == 'origin':
            git_url = words[1]
            break
    else:
        return "No origin remote found, abort"

    repo = git_url.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    remote_name = username
    remote_url = repo_git_url('%s/%s' % (username, repo))

    check_call(['git', 'remote', 'add', remote_name, remote_url])


def fetch(remote_name):
    check_call(['git', 'fetch', remote_name])
