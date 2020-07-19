import requests as req
import hashlib
import os
import json
import cloudscraper
from bs4 import BeautifulSoup

# TODO: reformat mod list or bring back glob
# TODO: nice curses ui
# TODO: async

# This class is supposed to be highly integrateable.
# You can change some behavior by simply creating subclass and overriding some methods

class MCBulkDownloader:
    def __init__(self, mld: list):
        self._scraper = cloudscraper.create_scraper()
        self.mld = mld

    # Downloads one mod
    def download_mod(self, modinfo):
        if modinfo['optional']:
            if not self.optional_ask('Do you want to download {}?'.format(modinfo['filename'])):
                return
        self.print_info('Downloading {}'.format(modinfo['filename']))
        if modinfo['link'].startswith('https://www.curseforge.com'):
            mod_screen = self._scraper.get(modinfo['link'], stream=True)

            soup = BeautifulSoup(mod_screen.text,features="html.parser")
            haslink = soup.findAll("p", {"class": "text-sm"})[0]

            mod_download = self._scraper.get("https://www.curseforge.com"+haslink.findAll("a", href=True)[0].get('href'),stream=True)
        else:
            mod_download = req.get(modinfo['link'], stream=True)
        with open('mods/'+modinfo['filename'], 'wb') as mod_file:
            for chunk in mod_download.iter_content(chunk_size=1024):
                mod_file.write(chunk)
                mod_file.flush()
            mod_file.close()
        self.print_info('Finished downloading {}'.format(modinfo['filename']))

    # Starts downloading mods from list
    def start_download(self):
        for mod in self.mld:
            filename = mod['filename']
            md5hash = mod['md5hash']

            if os.path.exists('mods/'+filename):
                with open('mods/'+filename, 'rb') as modfile:
                    calculated_hash = hashlib.md5(modfile.read()).hexdigest()
                    if calculated_hash == md5hash:
                        print('{} is up to date!'.format(filename))
                    else:
                        modfile.close()
                        os.remove('mods/'+filename)
                        self.download_mod(mod)
            else:
                self.download_mod(mod)

    # Override this method to change how to ask about optional mods
    @staticmethod
    def optional_ask(question):
        answer = input(question+' [Y/n]').lower()
        if answer in ['nope', 'nop', 'no', 'n']:
            return False
        elif answer in ['yes', 'ye', 'y', '']:
            return True
        else:
            return False

    # Override this method to change where to output progress info
    @staticmethod
    def print_info(msg: str):
        print(msg)

    # Takes url or file, parses its contents and passes mod list to MCBulkDownloader constructor
    @classmethod
    def from_url_or_file(cls, ml_source: str) -> bool:
        if os.path.exists(ml_source):
            with open(ml_source, 'r') as mlfile:
                mld = json.load(mlfile)
        else:
            # In case mod list is not a local file, but a url to a file. For example:
            #     'https://raw.githubusercontent.com/JohnTheCoolingFan/TBN3/master/modlistdownload.json'
            rqst = req.get(ml_source)
            if rqst.status_code == 200:
                mld = rqst.json()

        return cls(mld)


if __name__ == '__main__':
    mcbd = MCBulkDownloader.from_url_or_file('modlistdownload.json')
    mcbd.start_download()
