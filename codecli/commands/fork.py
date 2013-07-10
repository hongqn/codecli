from codecli.utils import check_call, repo_git_url, cd, merge_config


def populate_argument_parser(parser):
    parser.add_argument('upstream', help="name of upstream repo [e.g. dae]")
    parser.add_argument('origin', help="name of my fork [e.g. hongqn/dae]")
    parser.add_argument('dir', help="directory to clone")


def main(args):
    name = args.upstream
    check_call(['git', 'clone', repo_git_url(args.origin), args.dir])
    with cd(args.dir):
        merge_config()
        check_call(['git', 'remote', 'add', 'upstream', repo_git_url(name)])
