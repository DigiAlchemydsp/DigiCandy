#!/usr/bin/env python3
"""Generate every DigiScreen mod folder from ../art into ../mods.

Static images come from art/*.png; animations from art/anim/*.gif and
art/anim/*/ (a folder of PNG frames). Each becomes one mod per device.

    python gen_all.py [--dither] [--invert]
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_machine as mm   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'art')
MODS = os.path.join(ROOT, 'mods')


def sources():
    """-> list of (name, path), sorted, animations after statics."""
    out = []
    for f in sorted(glob.glob(os.path.join(ART, '*.png'))):
        out.append((os.path.splitext(os.path.basename(f))[0], f))
    for f in sorted(glob.glob(os.path.join(ART, 'anim', '*.gif'))):
        out.append((os.path.splitext(os.path.basename(f))[0], f))
    for f in sorted(glob.glob(os.path.join(ART, 'anim', '*.frames.bin'))):
        out.append((os.path.basename(f)[:-len('.frames.bin')], f))
    for d in sorted(glob.glob(os.path.join(ART, 'anim', '*'))):
        if os.path.isdir(d):
            out.append((os.path.basename(d), d))
    return out


def main():
    dither = '--dither' in sys.argv
    invert = '--invert' in sys.argv
    srcs = sources()
    if not srcs:
        print('no sources in', ART)
        return 1
    for name, path in srcs:
        for dev, suffix in ((mm.DT, 'dt'), (mm.DN, 'dn')):
            out = os.path.join(MODS, '%s-%s' % (name, suffix))
            _, n = mm.write_mod(out, name, path, dev, {'dither': dither,
                                                       'invert': invert})
            print('  %-14s %-3s %2d frame(s)' % (name, suffix, n))
    print('generated %d mods from %d sources' % (2 * len(srcs), len(srcs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
