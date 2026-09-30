# Building DigiScreen

## What you need

- **Python 3** with Pillow (`python -m pip install pillow`) — for the generator.
- An **elekloader** checkout — the SDK that turns a mod folder into an
  `.elemod`, and whose `core` mod the result depends on.
- The **m68k toolchain** (`m68k-elf-` or `m68k-linux-gnu-`). On Windows this
  tree uses `C:\sysgcc\m68k-elf` (GCC 4.8.0):

  ```sh
  export ELEKLOADER_CROSS=m68k-elf-
  export PATH=/c/sysgcc/m68k-elf/bin:$PATH
  ```

- The stock files, lawfully obtained:
  `Digitakt_OS1.53.syx` and `Digitone_and_Digitone_Keys_OS1.43.syx`.
- `core` mods built in the elekloader tree (`mods/core/out/core-2.1.elemod`,
  `mods/core-dn1/out/core-dn1-2.0a.elemod`).

This repository ships ready-built `.elemod`s in `releases/` and does **not**
distribute source images. To rebuild an overlay (or make your own) you bring
your own image and generate the mod folder first.

## 1. Generate a mod folder from your image

```sh
python tools/make_machine.py mylogo.png       -o mods/mylogo-dt
python tools/make_machine.py mylogo.png --dn  -o mods/mylogo-dn
```

A PNG, a GIF, or a folder of PNG frames (up to 60 frames). If you keep your
sources in an `art/` tree with the usual layout, `python tools/gen_all.py`
regenerates every mod at once.

## 2. Build the `.elemod`

```sh
python tools/build_all.py --elekloader ../elekloader \
    --dt-syx Digitakt_OS1.53.syx \
    --dn-syx Digitone_and_Digitone_Keys_OS1.43.syx
```

or one folder from the elekloader tree:

```sh
python -m elekloader.sdk.build ../DigiScreen/mods/mylogo-dt --stock Digitakt_OS1.53.syx
```

Expect `… .run 1284, .fast 0, .bss 0 bytes; 3 sites, 5 relocations`.

## 3. Patch a flashable `.syx`

Use a release from `releases/` (or your own freshly built `.elemod`). Digitakt:

```sh
cd elekloader
python -m elekloader.patch --stock Digitakt_OS1.53.syx \
    --mod mods/core/out/core-2.1.elemod \
    --mod ../DigiScreen/releases/planet1-dt.elemod \
    --out planet1-machine.syx --version 2.0z
```

Digitone:

```sh
python -m elekloader.patch --stock Digitone_and_Digitone_Keys_OS1.43.syx \
    --mod mods/core-dn1/out/core-dn1-2.0a.elemod \
    --mod ../DigiScreen/releases/planet1-dn.elemod \
    --out planet1-machine-dn.syx --version 2.0s
```

`patch` refuses overlaps, so a DigiScreen mod and a conflicting mod will be
caught. Recovery is the usual: hold `FUNC` while powering on, choose OS UPGRADE,
send the stock `.syx`.

## Conflicts

DigiScreen hooks the `queue_send` and present entries. It does not touch the
boot-intro call sites the splash mods use, so it should combine with them, but
it changes the present path globally — treat it as mutually exclusive with any
other mod that hooks `panel_diff` / `panel_flush` until tested.
