import os


class Manager:
    def __init__(self, shared_path: str, server_name: str, server_path: str):
        self.shared_path = shared_path
        self.server_name = server_name
        self.server_path = server_path

        # UNIX socket path
        self.sock_path = os.path.join(self.shared_path, f"{self.server_name}.sock")
        # Log path
        self.log_path = os.path.join(self.shared_path, f"{self.server_name}.txt")
    
    def start(self):
        with open(self.log_path, "w+") as fp:
            fp.write("Process forked and started the manager successfully!\n")
            fp.write(f"Socket path: {self.sock_path}, PID: {os.getpid()}\n")
            fp.close()
