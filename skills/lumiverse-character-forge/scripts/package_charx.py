"""Package a complete V3 card JSON as CHARX; optionally retain source ZIP assets."""
import argparse
import json
from pathlib import Path, PurePosixPath
import zipfile

MAX_TOTAL = 128 * 1024 * 1024


def safe_name(name):
    path = PurePosixPath(name)
    if not name or '\\' in name or path.is_absolute() or any(
        part in ('', '.', '..') or ':' in part for part in name.split('/')
    ):
        raise ValueError('Unsafe archive path: ' + name)
    return name


def read_archive(path):
    files = {}
    with zipfile.ZipFile(path) as archive:
        if sum(i.file_size for i in archive.infolist()) > MAX_TOTAL:
            raise ValueError('Archive exceeds 128 MiB uncompressed limit')
        for info in archive.infolist():
            if info.is_dir():
                safe_name(info.filename.rstrip('/'))
                continue
            name = safe_name(info.filename)
            if name in files or (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Duplicate or symbolic-link archive member: ' + name)
            files[name] = archive.read(info)
    return files


def validate(card, files):
    if not isinstance(card, dict) or card.get('spec') != 'chara_card_v3' or card.get('spec_version') != '3.0':
        raise ValueError('Expected chara_card_v3 / 3.0 envelope')
    data = card.get('data')
    if not isinstance(data, dict) or not isinstance(data.get('name'), str) or not data['name'].strip():
        raise ValueError('A nonempty data.name is required')
    for key in ('description', 'personality', 'scenario', 'first_mes', 'mes_example',
                'system_prompt', 'post_history_instructions', 'creator_notes',
                'creator', 'character_version', 'nickname'):
        if key in data and not isinstance(data[key], str):
            raise ValueError('Expected string: ' + key)
    for key in ('tags', 'alternate_greetings', 'group_only_greetings'):
        if key in data and (not isinstance(data[key], list) or not all(isinstance(x, str) for x in data[key])):
            raise ValueError('Expected string array: ' + key)
    if 'extensions' in data and not isinstance(data['extensions'], dict):
        raise ValueError('Expected extensions object')
    if 'character_book' in data:
        book = data['character_book']
        if not isinstance(book, dict) or not isinstance(book.get('entries'), list) or not all(isinstance(x, dict) for x in book['entries']):
            raise ValueError('Expected character_book with object entries')
    assets = data.get('assets', [])
    if not isinstance(assets, list):
        raise ValueError('Expected assets array')
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get('uri'), str):
            raise ValueError('Expected asset object with URI')
        uri = asset['uri']
        if uri.startswith(('embeded://', 'embedded://')):
            name = safe_name(uri.split('://', 1)[1])
            if name not in files:
                raise ValueError('Missing embedded asset: ' + name)


def package(card, output, source=None, assets_dir=None):
    files = read_archive(source) if source else {}
    if assets_dir:
        root = Path(assets_dir)
        if not root.is_dir():
            raise ValueError('Assets directory does not exist')
        for path in root.rglob('*'):
            if path.is_symlink():
                raise ValueError('Symbolic links are not accepted')
            if path.is_file():
                name = safe_name(path.relative_to(root).as_posix())
                if name == 'card.json' or name in files:
                    raise ValueError('Asset would overwrite existing member: ' + name)
                if path.stat().st_size + sum(map(len, files.values())) > MAX_TOTAL:
                    raise ValueError('Asset data exceeds size limit')
                files[name] = path.read_bytes()
    validate(card, files)
    files['card.json'] = json.dumps(card, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')
    if sum(map(len, files.values())) > MAX_TOTAL:
        raise ValueError('Package exceeds size limit')
    output = Path(output)
    if output.suffix.lower() != '.charx':
        raise ValueError('Output must end in .charx')
    # Exclusive creation prevents accidentally replacing a source or previous export.
    with output.open('xb') as handle:
        try:
            with zipfile.ZipFile(handle, 'w', zipfile.ZIP_DEFLATED) as archive:
                for name, contents in files.items():
                    archive.writestr(name, contents)
        except BaseException:
            handle.close()
            output.unlink(missing_ok=True)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('card_json', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--source-charx', type=Path, help='Retain all source members except replaced card.json')
    parser.add_argument('--assets-dir', type=Path, help='Directory containing archive-relative asset paths')
    args = parser.parse_args()
    try:
        card = json.loads(args.card_json.read_text(encoding='utf-8'))
        package(card, args.output, args.source_charx, args.assets_dir)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + '\n')
    print('Packaged CHARX; Lumiverse runtime compatibility requires separate evidence.')


if __name__ == '__main__':
    main()
