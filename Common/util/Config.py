import json
import os

from Common.Constants import IOS_APPLICATION_NAME, IOS_IPA_URI


class Config:
    def __init__(self):
        setting_uri = os.path.join(os.path.dirname(__file__), "../../Config/config.json")

        try:
            file = open(setting_uri, "r")
        except FileNotFoundError as e:
            print(e.strerror)
            raise

        self.systemConfig = json.loads(file.read())
        self.systemConfig[IOS_APPLICATION_NAME] = os.path.splitext(os.path.basename(self.systemConfig[IOS_IPA_URI]))[0]

        file.close()
