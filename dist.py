from os import walk
from math import ceil
import os.path as path
from zipfile import ZipFile, ZIP_DEFLATED


def exclude(s: str) -> bool:
    parts = s.split('/')
    reject = ('.git', '.github', 'tests', 'test')
    for r in reject:
        if r in parts:
            return True
    return False

to_archive = ['init.lua']

for (parent, _, files) in walk('pack'):
    for file in files:
        fullpath = path.join(parent, file).replace('\\', '/')
        if not exclude(fullpath):
            to_archive.append(fullpath)

archived = 0
with ZipFile('dist.zip', 'w', compression=ZIP_DEFLATED) as f:
    for file in to_archive:
        print(f'\r' + ' ' * 80 + '\r', end='', flush=True)
        p = ceil(archived/len(to_archive) * 100)
        print(f'Archiving {p}%', end='', flush=True)
        f.write(file)
        archived += 1
    print(f'\nDone ({len(to_archive)} files)')

