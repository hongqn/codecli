# encoding: UTF-8

import sys
import logging

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="commands",
                                       dest="subparser_command")
    subcommands = [
        ('fork', 'fork', "Create a fork"),
        ('start', 'start', "Start a new feature/bugfix branch"),
        ('sync', 'sync', "Sync branch with master"),
        ('pullreq', 'pullreq', "Send a pull request"),
    ]

    for command, module_name, help_text in subcommands:
        try:
            module = __import__('codecli.commands.' + module_name, globals(), locals(),
                                ['populate_argument_parser', 'main'])
        except ImportError:
            import traceback; traceback.print_exc()
            print >>sys.stderr, "Can not import command %s, skip it" % command
            continue

        subparser = subparsers.add_parser(command, help=help_text)
        subparser.add_argument('-v', '--verbose', action='store_true',
                               help="enable additional output")

        module.populate_argument_parser(subparser)
        subparser.set_defaults(func=module.main)

    argv = sys.argv[1:] or ['--help']
    args = parser.parse_args(argv)

    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=loglevel)

    return args.func(args)
