import os

from Common.Constants import *
from Builder.IOS.IOSBuilder import IOSBuilder
from Model.IOSComponent import IOSComponent
from Processes import OSCmdExecuter
from Processes.IOSProjectConfig import IOSProjectConfig


class IOSComponentBuilder(IOSBuilder):
    def __init__(self, config: IOSProjectConfig, component: IOSComponent):
        self.config = config
        self.component = component
        self.config_path_plist_uri = os.path.join(self.component.property.base_uri, PLIST)
        self.project_mobile_provision_uri = os.path.join(self.config.base_path, MOBILE_PROVISION)
        self.component_provision_uri = os.path.join(self.project_mobile_provision_uri,
                                                    self.component.property.name + MOBILE_PROVISION_EXTENSION)

    def reset(self):
        delete_code_signature = "rm -rf " + "\"" + self.component.property.base_uri + "/" + CODE_SIGNATURE + "\""
        OSCmdExecuter.run(delete_code_signature)

    def build(self):
        self.buildProperties()
        self.buildEntitlement()
        self.buildPListProperty()
        self.buildProvision()
        self.buildResignApp()

    def buildProperties(self):
        self.component.property.setTeamId(self.config.config[TEAM_ID])
        bundle_id_prompt = "Please Enter Builder ID for " + self.component.property.name + ": "
        self.component.property.setBundleId(input(bundle_id_prompt))

    def buildEntitlement(self):
        config_path_base_entitlement_folder_uri = os.path.join(self.config.base_path, ENTITLEMENTS)
        entitlement_file = self.component.property.name + ENTITLEMENTS_EXTENSION
        self.config_path_entitlement_uri = os.path.join(config_path_base_entitlement_folder_uri, entitlement_file)
        entitlement_cmd = "codesign -d --entitlements :- " + "\"" + self.component.property.base_uri \
                          + "\"" + " > " + "\"" + self.config_path_entitlement_uri + "\""

        OSCmdExecuter.run(entitlement_cmd)

        application_identifier = self.component.property.team_id + "." + self.component.property.bundle_id

        entitlement_prop_change = {APPLICATION_IDENTIFIER: application_identifier,
                                   APPLICATION_TEAM_IDENTIFIER: self.component.property.team_id}
        for key, value in entitlement_prop_change.items():
            entitlement_change = PLIST_BUDDY + " -c " + \
                                 "\"" + "SET " + key + " " + value + "\"" + " " + "\"" + \
                                 self.config_path_entitlement_uri + "\""

            OSCmdExecuter.run(entitlement_change)

    def buildPListProperty(self):
        plist_prop_change = {APPLICATION_BUNDLE_IDENTIFIER: self.component.property.bundle_id}
        for key, value in plist_prop_change.items():
            plist_change = PLIST_BUDDY + " -c " + \
                           "\"" + "SET " + key + " " + value + "\"" + " " + "\"" + \
                           self.config_path_plist_uri + "\""
            OSCmdExecuter.run(plist_change)

    def buildProvision(self):
        if not os.path.exists(self.component_provision_uri):
            print("Exiting Program missing file: " + self.component_provision_uri)
            raise

        application_provision_uri = os.path.join(self.component.property.base_uri, EMBEDDED_MOBILE_PROVISION)
        copy_provision_to_application = "cp " + "\"" + \
                                        self.component_provision_uri + "\"" + " " + "\"" + \
                                        application_provision_uri + "\""
        OSCmdExecuter.run(copy_provision_to_application)

    def buildResignApp(self):
        resign_component_cmd = "codesign -f -s " + "\"" + \
                               self.config.config[REGISTERED_CERTIFICATE] + \
                               "\"" + " " + "--entitlements" + " " + \
                               "\"" + self.config_path_entitlement_uri + "\"" + " " +\
                               "\"" + self.component.property.base_uri + "\""

        OSCmdExecuter.run(resign_component_cmd)
