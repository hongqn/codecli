from codecli.utils import check_call, repo_git_url, cd, merge_config


def populate_argument_parser(parser):
    parser.add_argument('repo', help="name of repo [e.g. dae]")
    parser.add_argument('dir', nargs='?', help="directory to clone to")


def main(args):
    cmd =['git', 'clone', repo_git_url(args.repo)]
    if args.dir:
        cmd.append(args.dir)
        dir = args.dir
    else:
        dir = args.repo.split('/')[-1]
    check_call(cmd)

    with cd(dir):
        merge_config()

        # set upstream to origin to make other code commands work
        check_call(['git', 'remote', 'add', 'upstream', repo_git_url(args.repo)])

