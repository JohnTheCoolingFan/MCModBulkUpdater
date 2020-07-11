import  requests
from git_clone import git_clone
import json
from git import Repo
servers = "https://raw.githubusercontent.com/Taruu/TANDOTS/master/server.json"

#TODO logger
class GetConfig:
    def __init__(self,Settings):
        self.Settings = Settings
        temp_result = requests.get(servers)
        if temp_result.status_code == 200:
            serverList = temp_result.json()

        listConf = self.Settings.allKeys()
        for serverLocal in listConf:
            if not(serverLocal in serverList):
                self.Settings.remove(serverLocal)
        for serverWeb in serverList:
            if not(serverWeb in listConf):
                self.Settings.setValue(serverWeb,{"name":serverWeb,"git":serverList[serverWeb],"path":None,"modList":None})
            else:
                if serverList[serverWeb] != self.Settings.value(serverWeb)["git"]:
                    tempServerSettings = self.Settings.value(serverWeb)
                    tempServerSettings["git"] = serverList[serverWeb]
                    self.Settings.setValue(serverWeb,tempServerSettings)


    def CloneGit(self,url,path,progressBar): #TODO progressBar add and etc...
        allZip = requests.get("url",steam=True)
        with open(allZip, 'wb') as mod_file:
            for chunk in allZip.iter_content(chunk_size=1024):
                mod_file.write(chunk)
                mod_file.flush()
            mod_file.close()



    def DownloadMods(self,serverName,path):

        with open("modlistdownload.json") as modlist_file:
            newModList = json.load(modlist_file)
        listConf = self.Settings.allKeys()
        if not (serverName in listConf):
            self.Settings.setValue(serverName,{"path": path,"ModList": newModList})
        else:
            dataServerConfig = self.Settings.value(serverName)
            oldModList = serverName["ModList"]


    def ConfigMods(self):
        pass
