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

args = vars(parser.parse_args())

files = glob.glob('*.jar')
files.sort()

with open(args['FILE'], 'r') as mlfile:
    mld = json.load(mlfile)
    for file in files:
        if file not in [mentry['filename'] for mentry in mld]:
            link = input('Download link for {}: '.format(file)).rstrip()
            md5hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
            mentry = dict(link=link, filename=file, md5hash=md5hash)
            if args['no-glob']:
                mglob = input('Glob for {}: '.format(file)).rstrip()
                mentry['glob'] = mglob
            mld.append(mentry)
        else:
            print('{} already in mod list. Skipping.'.format(file))
    print('Finished gathering info, writing changes to file.')
    mlfile.close()

with open(args['FILE'], 'w') as mlfile:
    json.dump(mld, mlfile, indent=4, sort_jeys=True)
    mlfile.close()
