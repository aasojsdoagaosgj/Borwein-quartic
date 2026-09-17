"""Check the frozen public repository bundle before replaying computations."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
for name, expected in manifest['sha256'].items():
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise RuntimeError('Invalid manifest path: ' + name)
    if not path.is_file():
        raise RuntimeError('Missing bundled file: ' + name)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError('Changed bundle content: ' + name)
print('All ' + str(len(manifest['sha256'])) + ' bundled files match their SHA-256 hashes.')
print('This verifies copied content, not the mathematical proof.')
