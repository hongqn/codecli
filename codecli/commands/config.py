from codecli.utils import get_config, set_config, del_config

CONFIG_KEYS = ['user.email', 'user.name', 'webbrowser.name']


def populate_argument_parser(parser):
    parser.add_argument('key', choices=CONFIG_KEYS)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('value', nargs='?')
    group.add_argument('--unset', action='store_true')


def main(args):
    if args.unset:
        del_config(args.key)
    elif args.value:
        set_config(args.key, args.value)
    else:
        print(get_config(args.key))
