import os

from Builder.IOS.IOSComponentBuilder import IOSComponentBuilder
from Common.Constants import *
from Builder.IOS.IOSBuilder import IOSBuilder
from Model.IOSApplication import IOSApplication
from Model.IOSComponent import IOSComponent
from Processes import OSCmdExecuter
from Processes.IOSProjectConfig import IOSProjectConfig


class IOSApplicationBuilder(IOSBuilder):
    def __init__(self, ios_project_config: IOSProjectConfig):
        IOSBuilder.__init__(self)
        self.ios_application = IOSApplication()
        self.ios_project_config = ios_project_config
        self.resigner_uri = self.ios_project_config.paths[RESIGN]
        self.payload_uri = os.path.join(self.resigner_uri, PAYLOAD_FOLDER)
        self.application_uri = os.path.join(self.payload_uri,
                                            self.ios_project_config.config[IOS_APPLICATION_NAME] + APP_EXTENSION)

        self.plugin_uri = os.path.join(self.application_uri, PLUG_INS)

        self.framework_uri = os.path.join(self.application_uri, FRAMEWORK)

    def reset(self):
        delete_framework = "cd " + "\"" + self.framework_uri + "\"" + "; rm -rf ./*/" + CODE_SIGNATURE
        OSCmdExecuter.run(delete_framework)

    def build(self):
        self.buildResignFramework()
        self.ios_application.property.setBaseUri(self.application_uri)
        self.ios_application.property.setComponentName(self.ios_project_config.config[IOS_APPLICATION_NAME])

        filenames = []
        for file in os.listdir(self.plugin_uri):
            if file.endswith(APPEX_EXTENSION):
                filenames.append(file)

        plugins = []

        for file_name in filenames:
            plugin = IOSComponent()
            plugin.property.setBaseUri(os.path.join(self.plugin_uri, file_name))
            plugin.property.setComponentName(os.path.splitext(os.path.basename(plugin.property.base_uri))[0])
            plugins.append(plugin)

        self.ios_application.plugins = plugins

        build_components = self.ios_application.plugins + [self.ios_application]

        for component in build_components:
            component_builder = IOSComponentBuilder(self.ios_project_config, component)
            component_builder.reset()
            component_builder.build()

        self.buildZipSolution()

    def buildResignFramework(self):
        resign_framework_cmd = "cd " + "\"" + self.framework_uri + "\"" + ";" + \
                               "codesign -f -s " + "\"" + \
                               self.ios_project_config.config[REGISTERED_CERTIFICATE] + "\"" + " " + "*"

        OSCmdExecuter.run(resign_framework_cmd)

    def buildZipSolution(self):
        resign_solution_uri = os.path.join(self.ios_project_config.base_path, RESIGN_SOLUTION)
        resign_solution_file_uri = os.path.join(resign_solution_uri,
                                                self.ios_project_config.config[IOS_APPLICATION_NAME] + IPA_EXTENSION)

        zip_solution_cmd = "cd " + "\"" + self.resigner_uri + "\"" + ";" + \
                           "zip -qr " + \
                           "\"" + resign_solution_file_uri + "\"" + " " + \
                           "\"" + PAYLOAD_FOLDER + "\"" + " " + \
                           "\"" + SWIFTSUPPORT_FOLDER + "\"" + " " + \
                           "\"" + SYMBOLS_FOLDER + "\""

        OSCmdExecuter.run(zip_solution_cmd)
