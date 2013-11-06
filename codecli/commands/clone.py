from codecli.utils import check_call, repo_git_url, cd, merge_config


def populate_argument_parser(parser):
    parser.add_argument('repo', help="url or name of repo [e.g. dae]")
    parser.add_argument('dir', nargs='?', help="directory to clone to")


def main(args):
    url = repo_git_url(args.repo)
    cmd = ['git', 'clone', url]

    if args.dir:
        cmd.append(args.dir)
        dir = args.dir
    else:
        dir = url.rsplit('/', 1)[-1].rpartition('.git')[0]

    check_call(cmd)

    with cd(dir):
        merge_config()

        # set upstream to origin to make other code commands work
        check_call(['git', 'remote', 'add', 'upstream', url])
