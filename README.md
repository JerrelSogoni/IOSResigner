# IOSResigner
#Requirements:
Python 3.9+, macOS

# To use the script
Initialize configurations in the config folder: config.json 

"config_path" - Absolute Path of your config folder for the project, any path you would like.

"team_id" : - This found in your apple developer account under Membersip Details "Team ID"

"ios_ipa_uri" : - Absolute path for your ipa file that needs to be resigned.

"registered_certificate" : - This is your certificate found and imported in your keychain access, typically, what your mobile provisions are associated with.

# Run the script and follow the instructions
*Each script run clears the area for a fresh install

You will be prompted to insert the necessary mobile provisions. This is typically the application mobile provision and the plugin provision.

Please downloaded mobile provision from apple for this application and assoicated plugins.

Please rename the mobile provision to the correct convention.

Typically the associated mobile provisions can be explored at your config_path/resigner/payload

There should be an application ipa assoicated wtih a mobile provision

Example of naming: Application -> Fred_s App.ipa => Fred_s App.mobileprovision

There are sometimes plugins found in config_path_resigner/payload/PlugIns, found with .appex extension

Example of naming: Plugin -> notify.appex => notify.mobileprovision

#When you are done with inserting the mobile provisions you can press enter to continue the resign process

There will be prompts to insert the bundle identifier, this can be found in the apple developer website under Certificates, Identifiers & Profiles: 
Click an identifier and check the Bundle ID

#Make sure all your information is correct, it should resign correctly
 The resulting resigned ipa is in config_path/resign_solutions/

Use the Apple Transporter and drag the IPA to upload the application to your app store!

Delete config_path folder if you would like
