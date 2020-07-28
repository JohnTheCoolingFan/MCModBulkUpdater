#!/usr/bin/env python3
import requests as req
import hashlib
import os
import json
import cloudscraper
from bs4 import BeautifulSoup

# TODO: nice curses ui
# TODO: async


# Exceptions
class MCBDError(Exception):
    """Base class for exceptions in this module"""

    def __init__(self):
        pass

class CFScrapeError(MCBDError):
    """Raised when scraping download from curseforge fails"""

    def __init__(self, filename, link, status_code):
        self.filename = filename
        self.link = link
        self.status_code = status_code

class ModDownloadError(MCBDError):
    """Raised when request for mod download fails"""

    def __init__(self, filename, link, status_code):
        self.filename = filename
        self.link = link
        self.status_code = status_code


# This class is supposed to be highly integrateable.
# You can change some behavior by simply creating subclass and overriding some methods
class MCBulkDownloader:
    def __init__(self, mld: list):
        self._scraper = cloudscraper.create_scraper()
        self.mld = mld
        self.errors = []

    def get_mod_download(self, modinfo):
        if modinfo['link'].startswith('https://www.curseforge.com'):
            mod_screen = self._scraper.get(modinfo['link'], stream=True)
            if mod_screen.status_code == 200:

                soup = BeautifulSoup(mod_screen.text,features="html.parser")
                haslink = soup.findAll("p", {"class": "text-sm"})[0]

                mod_download = self._scraper.get("https://www.curseforge.com"+haslink.findAll("a", href=True)[0].get('href'),stream=True)
            else:
                raise CFScrapeError(modinfo['filename'], modinfo['link'], mod_screen.status_code)
        else:
            mod_download = self._scraper.get(modinfo['link'], stream=True)

        return mod_download

    # Downloads one mod
    def download_mod(self, modinfo: dict):
        if modinfo['optional']:
            if not self.optional_ask(modinfo['filename']):
                return
        self.print_info('Downloading {}'.format(modinfo['filename']))
        try:
            mod_download = self.get_mod_download(modinfo)
        except CFScrapeError as cfse:
            self.print_info('Failed to scrape curseforge download page for {}. Status code: {}'.format(cfse.filename, cfse.status_code))
            self.errors.append(cfse)
        else:
            try:
                if mod_download.status_code == 200:
                    with open('mods/'+modinfo['filename'], 'wb') as mod_file:
                        for chunk in mod_download.iter_content(chunk_size=1024):
                            mod_file.write(chunk)
                            mod_file.flush()
                        mod_file.close()
                    self.print_info('Finished downloading {}'.format(modinfo['filename']))
                else:
                    raise ModDownloadError(modinfo['filename'], modinfo['link'], mod_download.status_code)
            except ModDownloadError as mde:
                self.print_info('Failed to download {}. Status code: {}'.format(mde.filename, mde.status_code))

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
        self.print_info('Finished downloading mods. Errors count: {}'.format(len(self.errors)))
        if len(self.errors) > 0:
            self.print_info('Failed mods: {}\n'.format('\n'.join([error.filename for error in self.errors])))
        self.errors = []

    # Override this method to change how to ask about optional mods
    @staticmethod
    def optional_ask(mod_name):
        answer = input('Do you want to download {}? [Y/n] '.format(mod_name)).lower()
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
    def parse_url_or_file(cls, ml_source: str) -> list:
        if os.path.exists(ml_source):
            with open(ml_source, 'r') as mlfile:
                mld = json.load(mlfile)
                mlfile.close()
        else:
            # In case mod list is not a local file, but a url to a file. For example:
            #     'https://raw.githubusercontent.com/JohnTheCoolingFan/TBN3/master/modlistdownload.json'
            rqst = req.get(ml_source)
            if rqst.status_code == 200:
                mld = rqst.json()

        return mld

    @classmethod
    def from_url_or_file(cls, ml_source: str):
        return cls(cls.parse_url_or_file(ml_source))

if __name__ == '__main__':
    mcbd = MCBulkDownloader.from_url_or_file('modlistdownload.json')
    mcbd.start_download()
