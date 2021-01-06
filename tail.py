import os
import sys
import time


class Tail:
    def __init__(self, tailed_file, interval_seconds=1.0, start_position="end"):
        self.tailed_file = os.path.abspath(tailed_file)
        self.check_file_validity()
        self.callback = sys.stdout.write
        if start_position not in ("start", "end"):
            raise Exception("start_position must be: start or end")
        self.start_position = start_position
        self.interval_seconds = interval_seconds

    def follow(self):
        deleted_once = False
        while True:
            if not self.check_file_validity(raise_error=False):
                deleted_once = True
                time.sleep(self.interval_seconds)
                continue
            with open(self.tailed_file, encoding="utf-8") as f:
                if deleted_once:
                    f.seek(0, os.SEEK_SET)
                elif self.start_position == "start":
                    f.seek(0, os.SEEK_SET)
                elif self.start_position == "end":
                    f.seek(0, os.SEEK_END)
                while True:
                    if not self.check_file_validity(raise_error=False):
                        deleted_once = True
                        break
                    line = f.readline()
                    if not line:
                        time.sleep(self.interval_seconds)
                    else:
                        self.callback(line)

    def register_callback(self, func):
        self.callback = func

    def check_file_validity(self, raise_error=True):
        if not os.access(self.tailed_file, os.F_OK):
            err = "File '%s' does not exist" % self.tailed_file
            if raise_error:
                raise Exception(err)
            else:
                print(err)
                return False
        if not os.access(self.tailed_file, os.R_OK):
            err = "File '%s' not readable" % self.tailed_file
            if raise_error:
                raise Exception(err)
            else:
                print(err)
                return False
        if os.path.isdir(self.tailed_file):
            err = "File '%s' is a directory" % self.tailed_file
            if raise_error:
                raise Exception(err)
            else:
                print(err)
                return False
        return True
