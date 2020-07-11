import glob
import json
import hashlib

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
    json.dump(mdl, mlfile)
    mlfile.close()
