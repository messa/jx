import argparse
from datetime import datetime
import logging
from pathlib import Path
import re
import socket
import yaml


logger = logging.getLogger(__name__)


def jx_main():
    p = argparse.ArgumentParser()
    p.add_argument('entry', nargs='*')
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    message = ' '.join(args.entry).strip()
    assert message

    from os.path import expanduser
    data_dir = Path(expanduser('~/.jx'))
    if not data_dir.exists():
        data_dir.mkdir()
        logger.info('Created directory %s', data_dir)

    entry_dir = data_dir / 'entries'
    if not entry_dir.exists():
        entry_dir.mkdir()

    day_file_name = 'day.{dt}.{hn}.yaml'.format(
        dt=datetime.now().strftime('%Y-%m-%d'),
        hn=get_hostname())
    day_file_path = entry_dir / day_file_name

    if day_file_path.exists():
        with day_file_path.open() as f:
            day_data = yaml.safe_load(f)
        assert isinstance(day_data['jx_day_records'], dict)
    else:
        day_data = {'jx_day_records': {}}

    day_entries = day_data['jx_day_records'].setdefault('entries', [])

    day_entries.append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': {
            'plaintext': message,
        },
    })

    tmp_path = day_file_path.with_name('.{}.tmp'.format(day_file_path.name))
    with tmp_path.open('w') as f:
        yaml.safe_dump(day_data, f, width=200, default_flow_style=False)
    tmp_path.rename(day_file_path)


def get_hostname():
    hn = socket.gethostname()
    safe = lambda c: re.match(r'^[a-zA-Z0-9_-]$', c)
    encode = lambda c: hex(ord(c)).lstrip('0')
    hn = ''.join((c if safe(c) else encode(c)) for c in hn)
    return hn
