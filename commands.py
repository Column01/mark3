import os
import sys
import asyncio
from manager import Manager

class BaseCommand:
    """ Base command class """
    def __init__(self):
        pass

    def execute(self, *args, **kwargs):
        pass


class StartCommand(BaseCommand):
    """ Command to start a server """
    def execute(self, server_path):
        # Get the server path
        self.server_path = server_path
        self.shared_path = "test/"
        # Verify it's actually a directory
        valid_path = self.verify_server_path()
        if valid_path:
            # Daemonize the process
            if self.daemonize():
                # Get the PID of the forked process and save it to a file
                with open(os.path.join(self.shared_path, f"{self.server_name}.pid"), 'w') as f:
                    f.write(f"{os.getpid()}\n")
                # Start an asyncio event loop
                loop = asyncio.get_event_loop()
                # Create an instance of the manager and call it's start method in the event loop
                manager = Manager(self.shared_path, self.server_name, self.server_path)
                _ = loop.call_soon(manager.start)

                # Start the event loop
                try:
                    loop.run_forever()
                finally:
                    loop.close()
                    sys.exit(0)
            sys.exit(0)
        else:
            exit(f"Invalid server path: {server_path}")

    def daemonize(self):
        """ Daemonizes the process to run in the background """
        if os.fork() > 0:
            # Parent process, we just wanna exit
            return False

        # Child process, time to do stuff
        os.chdir(".")
        os.setsid()
        null = os.open(os.devnull, os.O_RDWR)
        for fileno in (sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno()):
            try:
                os.dup2(null, fileno)
            except:
                pass
        return True

    def verify_server_path(self):
        if os.path.isdir(self.server_path):
            if self.server_path == ".":
                self.server_name = os.path.basename(os.getcwd())
            else:
                self.server_name = os.path.basename(self.server_path)
            return True
        else:
            return False
