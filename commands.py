import os
import sys
import asyncio
from manager import Manager

class BaseCommand:
    def __init__(self) -> None:
        self.servers = []

    def execute(self, *args, **kwargs):
        pass


class StartCommand(BaseCommand):
    def execute(self, server_path):
        self.server_path = server_path
        self.shared_path = "test/"
        valid_path = self.verify_server_path()
        if valid_path:
            if self.daemonize():
                with open(os.path.join(self.shared_path, f"{self.server_name}.pid"), 'w') as f:
                    f.write(f"{os.getpid()}\n")
                loop = asyncio.get_event_loop()
                manager = Manager(self.shared_path, self.server_name, self.server_path)
                manager.start()
                _ = loop.call_soon(manager.start)
                sys.exit(0)
            sys.exit(0)
        else:
            exit(f"Invalid server path: {server_path}")
    
    def daemonize(self):
        if os.fork() > 0:
            # Parent process, we just wanna exit
            return False

        # Child process, time to do stuff :D
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
            self.server_name = os.path.basename(self.server_path)
            return True
        else:
            return False
