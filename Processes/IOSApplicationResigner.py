from Builder.IOS.IOSApplicationBuilder import IOSApplicationBuilder
from Processes.IOSProjectConfig import IOSProjectConfig


class IOSApplicationResigner:
    def __init__(self):
        self.ios_project_config = IOSProjectConfig()
        self.ios_project_config.run()
        self.ios_application_builder = IOSApplicationBuilder(self.ios_project_config)

    def initialize(self):
        self.ios_application_builder.reset()

    def run(self):
        print("Please insert mobile provisions with correct naming convention.")
        input("Press Enter to continue resign process")
        self.ios_application_builder.build()
        print("Resign Completed!")
