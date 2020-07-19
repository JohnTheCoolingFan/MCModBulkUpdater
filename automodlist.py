import glob
import json
import hashlib
import argparse

# Place this file into your mods dir and run it
# It shoukd ask you for download link and glob (if enabled)
# After that it generates mod list

parser = argparse.ArgumentParser(description='Tool for easier creation of modlist.json')
parser.add_argument('FILE', required=True, help='File to use')
parser.add_argument('--no-glob', action='store_const', const=False, default=True, help='Don\'t ask for glob; Don\'t add glob')

files = glob.glob('*')
files.remove('automodlist.py')

with open('testconfig/modlistdownload.json', 'r') as mlfile:
    mdl = json.load(mlfile)
    for file in files:
        if file not in [mentry['filename'] for mentry in mdl]:
            link = input('Download link for {}: '.format(file)).rstrip()
            md5hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
            mglob = input('Glob for {}: '.format(file)).rstrip()
            mentry = dict(link=link, filename=file, md5hash=md5hash, glob=mglob)
            mdl.append(mentry)
        else:
            print('{} already in mod list. Skipping.'.format(file))
    print('Finished gathering info, writing changes to file.')
    mlfile.close()

with open('testconfig/modlistdownload.json', 'w') as mlfile:
    json.dump(mdl, mlfile, indent=4, sort_jeys=True)
    mlfile.close()
