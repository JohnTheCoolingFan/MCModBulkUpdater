import glob
import json
import hashlib
import argparse

# Place this file into your mods dir and run it
# It shoukd ask you for download link and glob (if enabled)
# After that it generates mod list

class ModListCreator:
    def __init__(self, filename: str, add_glob: bool):
        self.add_glob = add_glob
        self.filename = filename
        with open(filename, 'r') as mlfile:
            self.mld = json.load(mlfile)
            mlfile.close()

    def start(self):
        files = glob.glob('*.jar')
        files.sort()

        for file in files:
            self.add_mod(file)
        self.write()

    def add_mod(self, filename: str):
        if filename not in [mentry['filename'] for mentry in self.mld]:
            link = input('Download link for {}: '.format(filename)).rstrip()
            md5hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
            mentry = dict(link=link, filename=filename, md5hash=md5hash)
            if self.add_glob:
                mglob = input('Glob for {}: '.format(filename)).rstrip()
                mentry['glob'] = mglob
            self.mld.append(mentry)
        else:
            print('{} already in mod list. Skipping.'.format(filename))

    def write(self):
        with open(self.filename, 'w') as mlfile:
            json.dump(self.mld, mlfile, sort_keys=True, indent=4)

    @staticmethod
    def ask_link(filename: str) -> str:
        return input('Download link for {}: '.format(filename)).rstrip()

    @staticmethod
    def ask_glob(filename: str) -> str:
        return input('Glob for {}: '.format(filename)).rstrip()

    @staticmethod
    def ask_optl(filename: str) -> bool:
        answer = input('Is {} optional? [y/N] '.format(filename)).lower()
        if answer in ['no', 'n', '']:
            return False
        elif answer in ['yes', 'ye', 'y']:
            return True
        else:
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for easier creation of modlist.json')
    parser.add_argument('FILE', required=True, help='File to use')
    parser.add_argument('--no-glob', action='store_const', const=False, default=True, help='Don\'t ask for glob; Don\'t add glob')
    args = vars(parser.parse_args())

    mlc = ModListCreator(args['FILE'], args['no-glob'])
    mlc.start()
