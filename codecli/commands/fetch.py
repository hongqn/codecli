from commands import getoutput
from codecli.utils import check_call, repo_git_url


def populate_argument_parser(parser):
    parser.add_argument('username',
                        help="username of another fork of this repo")


def main(args):
    add_remote(args.username)
    fetch(args.username)


def add_remote(username):
    user_git_url = origin_git_url = None

    output = getoutput('git remote -v')
    for line in output.splitlines():
        words = line.split()
        if words[0] == 'origin':
            origin_git_url = words[1]
        if words[0] == username:
            user_git_url = words[1]

    if not origin_git_url:
        raise Exception("No origin remote found, abort")

    repo = origin_git_url.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    remote_name = username
    remote_url = repo_git_url('%s/%s' % (username, repo))

    if user_git_url:
        if user_git_url != remote_url:
            raise Exception("remote %s already exists, delete it first?")
        # already added
        return

    check_call(['git', 'remote', 'add', remote_name, remote_url])


def fetch(remote_name):
    check_call(['git', 'fetch', remote_name])
