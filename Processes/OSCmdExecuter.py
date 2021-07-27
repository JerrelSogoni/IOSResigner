import os


def run(cmd):
    if os.system(cmd) != 0:
        print("Failed to perform: " + cmd)
        raise
