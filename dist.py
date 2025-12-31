from os import walk
import gzip
import io
import os
from math import ceil
import os.path as path
# from zipfile import ZipFile, ZIP_DEFLATED
import tarfile

def exclude(s: str) -> bool:
    parts = s.split('/')
    reject = ('.git', '.github', 'tests', 'test')
    exts = ('.so', '.dll', '.dylib')

    for r in reject:
        if r in parts:
            return True

    for e in exts:
        if s.endswith(e):
            return True
    
    return False

to_archive = ['init.lua']

for (parent, _, files) in walk('pack'):
    for file in files:
        fullpath = path.join(parent, file).replace('\\', '/')
        if not exclude(fullpath):
            to_archive.append(fullpath)


print(f'Archiving {len(to_archive)} files')

archived = 0
buffer = io.BytesIO()

with tarfile.open(fileobj=buffer, mode='w') as f:
    for file in to_archive:
        p = ceil(archived/len(to_archive) * 100)
        f.add(file)
        archived += 1

data = buffer.getvalue()

print(f'Compressing {len(data) // 1024}KiB')
compressed = gzip.compress(buffer.getvalue(), compresslevel=9)

with open('dist.tar.gz', 'wb') as f:
    f.write(compressed)

print('Done')
