import argparse
from datetime import datetime
import logging
from os.path import expanduser
from pathlib import Path
import re
import socket
import yaml


logger = logging.getLogger(__name__)


def jx_main():
    p = argparse.ArgumentParser()
    p.add_argument('--list', '-l', action='store_true')
    p.add_argument('entry', nargs='*')
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    journal = Journal()

    if args.list:
        journal.show_entries()

    else:
        message = ' '.join(args.entry).strip()
        assert message
        journal.add_entry(message)



class Journal:

    def __init__(self):
        self._data_dir = Path(expanduser('~/.jx'))
        self._entry_dir = self._data_dir / 'entries'

    def _create_data_dir(self):
        if not self._data_dir.exists():
            self._data_dir.mkdir()
            logger.info('Created directory %s', self._data_dir)

    def _create_entry_dir(self):
        self._create_data_dir()
        if not self._entry_dir.exists():
            self._entry_dir.mkdir()

    def add_entry(self, message):
        day_file_name = 'day.{dt}.{hn}.yaml'.format(
            dt=datetime.now().strftime('%Y-%m-%d'),
            hn=get_hostname())
        day_file_path = self._entry_dir / day_file_name
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
        self._create_entry_dir()
        write_file(day_file_path, day_data)

    def show_entries(self):
        if not self._entry_dir.is_dir():
            return
        is_day_file_name = lambda s: s.startswith('day.') and s.endswith('.yaml')
        day_paths = [p for p in self._entry_dir.iterdir() if is_day_file_name(p.name)]
        all_entries = []
        for day_path in day_paths:
            with day_path.open() as f:
                day_data = yaml.safe_load(f)
            day_entries_raw = day_data['jx_day_records']['entries']
            for raw_entry in day_entries_raw:
                all_entries.append(Entry(raw_entry))
        all_entries.sort(key=lambda entry: entry.date)
        for entry in all_entries:
            print('{}: {}'.format(entry.date, entry.message))


class Entry:

    def __init__(self, raw_entry):
        self.date = datetime.strptime(raw_entry['date'],'%Y-%m-%d %H:%M:%S')
        self.message = raw_entry['message']['plaintext']


def write_file(path, content):
    assert not isinstance(content, bytes)
    if not isinstance(content, str):
        content = yaml.safe_dump(content, width=200, default_flow_style=False)
    tmp_path = path.with_name('.{}.tmp'.format(path.name))
    with tmp_path.open('w') as f:
        f.write(content)
    tmp_path.rename(path)


def get_hostname():
    hn = socket.gethostname()
    safe = lambda c: re.match(r'^[a-zA-Z0-9_-]$', c)
    encode = lambda c: hex(ord(c)).lstrip('0')
    hn = ''.join((c if safe(c) else encode(c)) for c in hn)
    return hn
