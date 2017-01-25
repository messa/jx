import argparse
from pathlib import Path


def jx_main():
    p = argparse.ArgumentParser()
    p.add_argument('entry', nargs='*')
    args = p.parse_args()
    assert 0, repr(args)
