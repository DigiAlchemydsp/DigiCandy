# How DigiScreen works

The main OS on both targets loads at `0x40000400`. Addresses below are runtime
addresses (subtract `0x40000400` for a file offset in decompressed section 3).
The Digitakt uses OS 1.53, the Digitone 1.43.

DigiScreen installs three `jmp` sites. Each replaces a function entry with a
jump to a stub in the mod's `.run` section; the stub does its work, replays the
few stock instructions it displaced, and jumps back.

## 1. The combo (`queue_send` entry)

Every UI event is queued by `queue_send(queue, item)`, which stores the **item
pointer**. A key event is a 16-byte record:

| offset | size | meaning |
|---|---|---|
| `+0` | 1 | type; `0` = key, `5` = timer tick |
| `+4` | 4 | control code |
| `+8` | 4 | flags — `0x01` press, `0x02` chord, `0x08` repeat, `0x10` release |
| `+c` | 4 | timestamp |

The stub only looks at events delivered to the UI queue. Control codes are the
**runtime** codes (measured), *not* the firmware's 48-entry panel-test table,
which labels a different numbering:

| | modifier | YES |
|---|---|---|
| Digitakt 1.53 | `TRK` = 2 | `YES` = 12 |
| Digitone 1.43 | `MIDI` = 2 | `YES` = 13 |

The stub ignores repeat events (`0x08`) entirely, so holding a key does not
retrigger. It uses a one-shot latch: a modifier **press** sets the latch, and
the next YES **press** toggles the overlay and clears it; any release also
clears it. So YES alone never triggers, and a missed release cannot stick —
the latch always clears itself by the next YES.

## 2. Drawing (`panel_diff` / `panel_flush` entry)

When the overlay is on, the stub copies the current 1024-byte frame from
`frames.bin` into the front buffer pointed to by the `fb_front` global, then
runs the stock present. A frame index advances once per present (mod the frame
count), so a multi-frame input animates. The firmware redraws the UI normally;
DigiScreen covers each composed frame, so the machine keeps running underneath
and nothing is drawn once the overlay is off. Both presents are hooked because
the UI uses either.

## Addresses

| | Digitakt 1.53 | Digitone 1.43 |
|---|---|---|
| `queue_send` | `0x40001b7a` | `0x40001cda` |
| … `+8` (return) | `0x40001b82` | `0x40001ce2` |
| `ui_queue` | `0x4060fc28` | `0x4052a6bc` |
| `panel_diff` | `0x400e60e2` | `0x400f8efa` |
| `panel_flush` | `0x400e6064` | `0x400f8e7c` |
| `fb_front` | `0x4020d8f8` | `0x40241a44` |

The displaced prologues the stubs replay:

- `queue_send`: `move.l %a2,-(%a7)` / `move.l %d2,-(%a7)` / `movea.l 0xc(%a7),%a0`
- `panel_diff`: `lea.l -0x28(%a7),%a7` / `movem.l %d2-%d6/%a2-%a4,(%a7)`
- `panel_flush`: `lea.l -0x1c(%a7),%a7` / `movem.l %d2-%d5/%a2,(%a7)`

## Panel format

128x64, 1 bit per pixel, 1024 bytes. `byte = page + 8*column`, with
`page = 7 - (y>>3)` and `bit = y & 7` (LSB first). The mod multiplies the
column by 8 and ORs the bit — see `tools/make_machine.py:pack`.

## Resources

`.run` is 1284 bytes (code + 1024-byte frame + three state words) and needs the
`core` mod, which sets up the RAM. No imports; five relocations (the absolute
symbol addresses).

## Status

Built and linted against the Digitakt 1.53 stock, and tested on hardware. The
key-record layout is shared Elektron UI framework behaviour
(documented for Digitakt II in `digiemu-main/emu/uitrace.py`), and the runtime
key codes come from the measured device maps in `digiemu-main/devices/`.

## Revisions

- **1.0 (fixed).** The first cut toggled on every press event while both keys
  were considered held, so key repeats re-fired it and a missed modifier release
  left it stuck (then YES alone toggled). Repeats are now ignored (`0x08`) and
  the modifier is a one-shot latch that any release or the next YES clears.
- Multi-frame animation added (`aba`, `digitrash`).
