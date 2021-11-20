import argparse


def init_parser():
    parser = argparse.ArgumentParser(prog="mark3", description="An asynchronous Minecraft server wrapper written in python3")
    sub_parsers = parser.add_subparsers()

    start_parser = sub_parsers.add_parser("start", help="The start command")
    start_parser.add_argument("-p", "--path", metavar="path", type=str, help="the path to the server directory")
    start_parser.set_defaults(command="start")

    attach_parser = sub_parsers.add_parser("attach", help="attaches to a server")
    attach_parser.add_argument("-n", "--name", metavar="name", type=str, help="the name of the server")
    attach_parser.set_defaults(command="attach")

    return parser

def main():
    parser = init_parser()
    # Get arguments from command
    args = parser.parse_args()
    print(args)
    if args.command == "start":
        if args.path is None:
            path = "."
        else:
            path = args.path
        print(f"Start command! Path: {path}")
        from commands import StartCommand
        cmd = StartCommand()
        cmd.execute(path)
    if args.command == "attach":
        print("ATTACH COMMAND!")

if __name__ == "__main__":
    main()
