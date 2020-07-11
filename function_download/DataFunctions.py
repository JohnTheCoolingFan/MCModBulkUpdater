import  requests

servers = "https://raw.githubusercontent.com/Taruu/TANDOTS/master/server.json"

class GetConfig:
    def __init__(self):
        pass

    def Setting(self,Settings):
        listConf = Settings.allKeys()
        if not("oldservers" in listConf):
            temp_result = requests.get(servers)
            Settings.setValue("oldservers",)
        for server in Settings.value("oldservers"):
            if not(server in listConf):
                Settings.setValue(server,requests.get(Settings.value("oldservers")[server]).json())
            print("servers",server,)



    def ConfigMods(self):
        pass
