# Releases

Built `.elemod` files, one per source per device. `-dt` is Digitakt mk1
(OS 1.53), `-dn` is Digitone mk1 / Keys (OS 1.43).

These are the DigiScreen overlay releases.

| file | frames |
|---|---|
| `planet1-dt.elemod` / `planet1-dn.elemod` | 1 |
| `catbooting-…` | 1 |
| `mount-…` | 1 |
| `pfft-…` | 1 |
| `aba-…` | 3 |
| `digitrash-…` | 15 |
| `loox-…` | 35 |
| `tussy-…` | 59 |
| `bzme-…` | 14 |
| `reach-…` | 18 |
| `claw-…` | 18 |
| `tidemoon-…` | 60 |

Each needs the matching `core` mod and is installed by patching a stock `.syx`:

```sh
cd elekloader
python -m elekloader.patch --stock Digitakt_OS1.53.syx \
    --mod mods/core/out/core-2.1.elemod \
    --mod ../DigiScreen/releases/planet1-dt.elemod \
    --out digiscreen.syx --version 2.0z
```

Once installed, `TRK+YES` (Digitakt) / `MIDI+YES` (Digitone) toggles the
overlay. The overlays are built from the project's own sources, which are not
distributed; rebuild your own with `tools/make_machine.py` +
`tools/build_all.py`.
