import  requests

servers = "https://raw.githubusercontent.com/Taruu/TANDOTS/master/server.json"

class GetConfig:
    def __init__(self):
        pass

    def Setting(self,Settings):
        listConf = Settings.allKeys()
        if not("oldservers" in listConf):
            temp_result = requests.get(servers)
            if temp_result.status_code == 200:
                Settings.setValue("oldservers",temp_result.json())
            else:
                return "Not servers config" #TODO init this error
        for server in Settings.value("oldservers"):
            if not(server in listConf):
                temp_result = requests.get(Settings.value("oldservers")[server]).json()
                if temp_result.status_code == 200:
                    Settings.setValue(server,temp_result.json())
                else:
                    return "Not config server!"



    def ConfigMods(self):
        pass
