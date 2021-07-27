import os
import shutil

from Common.Constants import *
from Common.util.Config import Config
from Processes import OSCmdExecuter
from Validator.Processes.IOSProjectInitializerValidator import IOSProjectInitializerValidator


class IOSProjectConfig:
    def __init__(self):
        self.config = Config().systemConfig
        self.ios_project_initializer_validator = IOSProjectInitializerValidator()

        self.folders = [MOBILE_PROVISION, ENTITLEMENTS, RESIGN,
                        RESIGN_SOLUTION]
        paths = {}
        self.base_path = os.path.join(self.config[CONFIG_PATH], BASE_FOLDER)
        paths[BASE_FOLDER] = self.base_path
        for folder in self.folders:
            paths[folder] = os.path.join(self.base_path, folder)

        self.paths = paths

    def run(self):
        if not self.ios_project_initializer_validator.validate(self.paths.values()):
            print("Project space is being used, Deleting for fresh install")
            try:
                shutil.rmtree(self.base_path)
            except OSError as e:
                print("Error: %s : %s" % (self.base_path, e.strerror))
                raise

        print("Creating Project Folders")
        for path in self.paths.values():
            os.mkdir(path)
            print("Folder Created: '%s'" % path)

        print("unzipping ipa into project folders")
        unzip_cmd = "unzip " + "\"" + self.config[IOS_IPA_URI] + "\"" + \
                    " -d " + "\"" + os.path.join(self.base_path, RESIGN) + "\""

        OSCmdExecuter.run(unzip_cmd)

        print("Project initialized successfully")
        print("Please add mobile_provision associate with project to the %s folder" % MOBILE_PROVISION)
