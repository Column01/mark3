import json
import logging
import os
from collections import OrderedDict


class Mark2Config(OrderedDict):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as fp:
                data = json.load(fp)
                for k, v in data.items():
                    self[k] = v
                fp.close()
        logging.info(f"Loaded mark2 config from disk: {self.file_path}")
