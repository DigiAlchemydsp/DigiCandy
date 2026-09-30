# tools

These tools build **Display** overlays: the generated mod hooks the
`queue_send` key queue and the `panel_diff` / `panel_flush` presents to toggle a
full-panel image over the **live UI** (`"category": "Display"`, combo
`TRK+YES` / `MIDI+YES`).

They are **not** the DigiSplash boot-splash toolchain. DigiSplash's
`make-bootanim` emits `"category": "Boot"` mods that draw over the *intro*;
this repo's tools never touch the intro sites.

| | |
|---|---|
| `make_machine.py` | one image -> one mod folder (`mod.json`, `splash.s`, `frames.bin`, `README.md`) |
| `gen_all.py` | every `art/*.png` -> `mods/<image>-dt` and `-dn` (local `art/` tree) |
| `build_all.py` | every `mods/*` -> `.elemod` via elekloader's SDK |

```sh
python make_machine.py mylogo.png      -o mods/mylogo-dt
python make_machine.py mylogo.png --dn -o mods/mylogo-dn [--name NAME] [--dither] [--invert]

python gen_all.py            # regenerate every mod from a local art/ tree

python build_all.py --elekloader ../elekloader \
    --dt-syx Digitakt_OS1.53.syx --dn-syx Digitone_and_Digitone_Keys_OS1.43.syx
```

Source images are not part of this repository: supply your own PNG/GIF/frames
(or keep them in a local, git-ignored `art/` tree). The device tables
(addresses, key codes, displaced-stock bytes) live at the top of
`make_machine.py`; `gen_all.py` and `build_all.py` only need Python plus the
files you generate.
