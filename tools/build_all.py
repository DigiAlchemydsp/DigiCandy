#!/usr/bin/env python3
"""Build every DigiScreen mod folder with elekloader's SDK.

    python build_all.py --elekloader ../elekloader \
        --dt-syx Digitakt_OS1.53.syx --dn-syx Digitone_and_Digitone_Keys_OS1.43.syx

Put the m68k toolchain on PATH first (see ../docs/BUILDING.md).
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS = os.path.join(ROOT, 'mods')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--elekloader', required=True)
    ap.add_argument('--dt-syx', required=True)
    ap.add_argument('--dn-syx', required=True)
    a = ap.parse_args()
    only = [d for d in sorted(os.listdir(MODS))
            if os.path.exists(os.path.join(MODS, d, 'mod.json'))]
    failed = 0
    for d in only:
        mod = json.load(open(os.path.join(MODS, d, 'mod.json')))
        syx = a.dt_syx if mod['device'] == 'digitakt-mk1' else a.dn_syx
        cmd = [sys.executable, '-m', 'elekloader.sdk.build',
               os.path.join(MODS, d), '--stock', syx]
        print('== %s (%s)' % (d, mod['device']))
        r = subprocess.run(cmd, cwd=a.elekloader)
        failed += r.returncode != 0
    print('%d mods, %d failed' % (len(only), failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
