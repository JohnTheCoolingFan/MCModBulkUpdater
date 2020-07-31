import mcbulkdownloader as mcbd
import requests as req
import hashlib
import json
import os

class ModDownloadURLError(mcbd.MCBDError):
    def __init__(self, filename, link, status_code):
        self.filename = filename
        self.link = link
        self.status_code = status_code

class MCBulkDownloaderV2(mcbd.MCBulkDownloader):
    def __init__(self, mp_info: dict):
        self.req = req.Session()
        self.mp_name = mp_info['name']
        self.mod_list = mp_info['modlist']

    def get_mod_download(self, modinfo: dict) -> req.Request:
        filename = modinfo['filename']

        md_url_get = 'https://addons-ecs.forgesvc.net/api/v2/addon/{addonID}/file/{fileID}'.format(addonID=modinfo['addonID'], fileID=modinfo['fileID'])
        mod_download_url = self.req.get(md_url_get)

        if mod_download_url.status_code == 200:
            mod_download = self.req.get(mod_download_url.text, stream=True)
            if mod_download.status_code == 200:
                return mod_download
            else:
                raise mcbd.ModDownloadError(filename, mod_download_url.text, mod_download.status_code)
        else:
            raise ModDownloadURLError(filename, md_url_get, mod_download.status_code)

    def download_mod(self, modinfo: dict):
        filename = modinfo['filename']
        optional = modinfo['optional']

        if optional:
            if not self.optional_ask(filename):
                return
        self.print_info('Downloading {}'.format(filename))
        mod_download = self.get_mod_download(modinfo)
        with open('mods/'+filename, 'wb') as mod_file:
            for chunk in mod_download.iter_content(chunk_size=1024):
                mod_file.rite(chunk)
                mod_file.flush()
            mod_file.close()
        self.print_info('Finished downloading {}'.format(modinfo['filename']))

    def start_download(self):
        for mod in self.mod_list:
            filename = mod['filename']
            #md5hash = mod['md5hash']
            md5hash = 'test'

            if os.path.exists('mods/'+filename):
                with open('mods/'+filename, 'rb') as mod_file:
                    calculated_hash = hashlib.md5(mod_file.read()).hexdigest()
                    if calculated_hash == md5hash:
                        print('{} is up to date!'.format(filename))
                    else:
                        mod_file.close()
                        os.remove('mods/'+filename)
                        self.download_mod(mod)
            else:
                self.download_mod(mod)
        self.print_info('Finished downloading mods.')

    @classmethod
    def parse_url_or_file(cls, ml_source: str) -> dict:
        mp_source = ml_source
        if os.path.exists(mp_source):
            with open(mp_source, 'r') as mp_file:
                mp_info = json.load(mp_file)
                mp_file.close()
        else:
            rqst = req.get(mp_source)
            if rqst.status_code == 200:
                mp_info = rqst.json()

        return mp_info

if __name__ == '__main__':
    mcbdv2 = MCBulkDownloaderV2.from_url_or_file('modlistv2.json')
    mcbdv2.start_download()
