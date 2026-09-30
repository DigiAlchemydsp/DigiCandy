# Notice

This project is **independent and is not affiliated with or endorsed by
Elektron**. Digitakt, Digitone and Elektron are trademarks of their respective
owners.

## No firmware

No Elektron firmware is included, and none should ever be committed. The mods
contain only their own code plus short stock-byte excerpts and hashes used to
verify the patch sites; they are applied to a stock `.syx` you obtain yourself.
The `.gitignore` excludes firmware and anything derived from it (`*.syx`,
`*.snap`, cards).

## Code licence

The `.elemod` files and the tools here are **GPL-2.0-or-later** (see
[LICENSE](LICENSE)), matching elekloader, which they are built for.

## Assets

The images shown by the overlays are provided **for personal, educational and
non-commercial use only**. **No source GIFs or images are distributed** in this
repository — only the built `.elemod` files and the tools needed to build your
own from your own source material.

Several overlays were derived from third-party GIFs; their upstream copyright is
unverified:

| mod | source |
|---|---|
| `loox` | `1_CqtKSeLhUEUfiXsnYMqfbQ.gif` |
| `tussy` | `Primp.gif` |
| `reach` | `0efb8c5f30bf27f2dfa56cf4bbfb6256.gif` |
| `claw` | `b6906df95f98f9324583601d7f9dcd8d.gif` |
| `tidemoon` | `Qd87v2.gif` |

The GPL above applies only to the project's own code and tools. If you hold
rights to any material and want it removed, open an issue.

## Credit

Container-format and patching knowledge derives from **elekloader** and the
**digiemu** reverse-engineering work.
