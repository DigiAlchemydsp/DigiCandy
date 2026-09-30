# Installing DigiCandy (building a flashable `.syx`)

DigiCandy is a full-panel **overlay**: it hooks the panel present path, so
install **one overlay at a time**. Each overlay needs the matching `core` mod
and a stock OS file you obtain yourself.

## What you need

- **elekloader** ([github.com/irpina/elekloader](https://github.com/irpina/elekloader))
  with its `core` mods built: `mods/core/out/core-2.1.elemod` (Digitakt) and
  `mods/core-dn1/out/core-dn1-2.0a.elemod` (Digitone).
- The stock OS: `Digitakt_OS1.53.syx` (Digitakt mk1) or
  `Digitone_and_Digitone_Keys_OS1.43.syx` (Digitone mk1 / Keys).
- **Elektron Transfer** (or any SysEx/MIDI file sender) to flash.
- To build your own: Python 3 + Pillow and the m68k toolchain — see
  [BUILDING.md](BUILDING.md).

## 1. Patch a stock OS

Digitakt (`-dt`):

```sh
cd elekloader
python -m elekloader.patch --stock Digitakt_OS1.53.syx \
    --mod mods/core/out/core-2.1.elemod \
    --mod ../DigiCandy/releases/planet1-dt.elemod \
    --out digicandy.syx --version 2.0z
```

Digitone (`-dn`):

```sh
python -m elekloader.patch --stock Digitone_and_Digitone_Keys_OS1.43.syx \
    --mod mods/core-dn1/out/core-dn1-2.0a.elemod \
    --mod ../DigiCandy/releases/planet1-dn.elemod \
    --out digicandy-dn.syx --version 2.0s
```

`patch` refuses overlaps, so it will catch a conflicting mod.

## 2. Flash it (OS UPGRADE)

1. Connect the device over USB (or MIDI DIN in/out).
2. Power the device **off**.
3. Hold **`FUNC`** while powering on to reach the startup menu.
4. Choose **`OS UPGRADE`** (on the Digitakt/Digitone menu this is `TRIG 4`).
5. In **Elektron Transfer**, send the patched `digicandy.syx`.
6. When it reboots, the version string shows `2.0z` / `2.0s` (your `--version`).

**Recovery:** hold `FUNC` on power-up, choose `OS UPGRADE`, and send the **stock**
`.syx` back. Only the main OS section changes, so the bootstrap and updater stay
stock.

## 3. Use it

- **Digitakt:** `TRK` + `YES` toggles the overlay.
- **Digitone:** `MIDI` + `YES`.

Press the combo again to remove it. See the *Easter Egg* and *Known bugs*
sections in the [README](../README.md).

## Conflicts

DigiCandy hooks the panel present entry globally. Install **one** DigiCandy
overlay; treat it as mutually exclusive with any other mod that hooks
`panel_diff` / `panel_flush` until tested. It does not touch the boot-intro call
sites the splash mods use, so it should combine with those.
