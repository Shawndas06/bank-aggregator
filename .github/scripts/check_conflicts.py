"""Reject unresolved merge markers in tracked text, independent of filename encoding."""
import re
import subprocess
from pathlib import Path

pattern = re.compile(rb'^(?:<{7} .+|={7}|>{7} .+|\|{7} .+)$', re.MULTILINE)
failed = []
for filename in subprocess.check_output(['git', 'ls-files', '-z']).split(b'\0'):
    if not filename:
        continue
    path = Path(filename.decode('utf-8', errors='surrogateescape'))
    if not path.is_file():
        continue
    content = path.read_bytes()
    if b'\0' not in content and pattern.search(content):
        failed.append(str(path))
if failed:
    raise SystemExit(f'Unresolved conflict markers: {failed}')
print('No unresolved conflict markers')
