from codecli.utils import (check_call, repo_git_url, cd, merge_config,
                           print_log, get_code_username, log_error)


def populate_argument_parser(parser):
    parser.add_argument('upstream', help="name of upstream repo [e.g. dae]")
    code_username = get_code_username()
    if code_username:
        parser.add_argument('origin', nargs='?',
                            help="name of my fork [e.g. hongqn/dae] "
                                 "[default %s/UPSTREAM]" % code_username)
    else:
        parser.add_argument('origin',
                            help="name of my fork [e.g.  hongqn/dae]")
    parser.add_argument('dir', nargs='?', help="directory to clone")


def main(args):
    name = args.upstream

    if not args.origin:
        code_username = get_code_username()
        if not code_username:
            log_error('origin not specified')
            return 1
        args.origin = '%s/%s' % (code_username, name)

    if not args.dir:
        args.dir = name.rsplit('/')[-1]
        print_log("Destination dir is not specified, will use {}".format(args.dir))

    check_call(['git', 'clone', repo_git_url(args.origin), args.dir])
    with cd(args.dir):
        merge_config()
        check_call(['git', 'remote', 'add', 'upstream', repo_git_url(name)])
