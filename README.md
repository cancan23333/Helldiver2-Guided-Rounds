# Guided Rounds / 制导弹药

**English** | [简体中文](README.zh-CN.md)

> Full manual: [English](docs/README.en.md) · [中文](docs/README.md)

Guided Rounds brings the P-92 Warrant's homing behaviour to every weapon in your
arsenal. A round leaves the barrel, finds a target in the aim cone and steers
onto it — while **damage, muzzle velocity and ballistics stay the weapon's own
values**. It ships an aim-range ring, lock markers, a target box, and a full
in-game **MODS** menu, all live-adjustable.

- Authors: **cancan2333 & SoS2430**
- Requires: **Bingus Shared Loader v15+**, **HD2Runtime 0.31.x**,
  **Vanilla Plus Megapack** (it provides the in-game MODS menu)
- Source: `docs/guided_rounds.lua` · Build: `build.py`

---

## What's new in v1.9.12

**Some Illuminate units — mostly Voteless — could not be locked.** The live log
showed the cause: a Voteless carries a second health record for its decaying
"constitution" value, and that record reports `status=1` while the body is very
much alive. The old dead-cache treated any non-zero status as death and removed
the whole unit from the target list for 60 seconds, over and over.

- The dead cache now only honours **`status=2`** (the real death record), and
  never honours a hit on a body-part row.
- A bone that reads as exactly `(0,0,0)` is treated as unreadable, so a swapped
  skeleton can no longer park a target at the world origin.
- `debug=1` now prints `dead=` and `status=` on the WATCH line, so the next
  occurrence is one glance away.

See the [changelog](docs/README.md#版本历史) for v1.9.11 (per-weapon priority)
and v1.9.0 (category pages).

## Install

1. Install the mod loader: [HD2 Arsenal](https://www.nexusmods.com/helldivers2/mods/4664).
2. In HD2 Arsenal, import `Guided-Rounds-v1.9.12.zip` and make sure these are
   installed too:
   - [Bingus Shared Loader](https://ayakamods.com/mods/bingus-shared-loader.3861/)
   - [hd2runtime](https://ayakamods.com/mods/hd2runtime.4260/)
   - [Vanilla Plus Megapack](https://www.nexusmods.com/helldivers2/mods/16294) — required, it provides the MODS menu
3. Load order, top to bottom (any other order and the addon does nothing):

   ```
   Guided Rounds
   Vanilla Plus Megapack
   Bingus Shared Loader
   hd2runtime
   ```
4. Launch the game. The menu is **Esc → MODS**, page `01 · GUIDED ROUNDS`.

Without hd2runtime the leased projectile material does not load and rounds show
up as a purple missing-material icon.

## Menu at a glance

| Page | Contents |
| --- | --- |
| `01 · GUIDED ROUNDS` | Master switch, aim cone, lock range, refresh rate, ballistics |
| `02 · GUIDED EXPLOSIVE FUSE` | Fuse / airburst timers for explosive rounds |
| `03–11 · GUIDED <WEAPON CLASS>` | Per-weapon lock switch + aim mode, 9 classes, 32 rows per page |
| `12 · GUIDED WEAPON PRIORITY` | Pick which weapon the target-priority pages edit |
| `13 · GUIDED TARGET PRIORITY` | Manual priority master switch |
| `14+ · GUIDED TERMINIDS / AUTOMATONS / ILLUMINATE / OTHER` | One 0–9 slider per enemy |

## Three layers of targeting priority

1. **Per weapon, coarse** (pages 03–11): OFF, aim-first, biggest-health-first,
   smallest-health-first.
2. **Global table** (pages 13–19, `tp_<target>=0-9`): 1 locks first, 9 last.
3. **Per weapon table** (page 12 + pages 13–19, `wpw_<weapon>_<target>=0-9`):
   enables when `wpc_<weapon>=1`; a target the weapon does not set falls back to
   the global table. **0 means "not set" in both layers.**

## Configuration

`%LOCALAPPDATA%\Hd2ApwGuidance\apw_guidance.cfg` (edited by the menu, safe to
edit by hand with the game closed):

| Key | Meaning |
| --- | --- |
| `enable=0/1` | Master switch, same as the menu toggle and F7 |
| `weapons=0x…,…` | Weapons that are guided (the menu writes this) |
| `prio_targets=` / `prio_small=` | Weapons that prefer biggest / smallest enemy |
| `prio_manual=0/1` | Manual priority master switch |
| `tp_<16 hex>=0-9` | Global per-target priority |
| `wpc_<16 hex weapon>=1` | Turn on that weapon's own table |
| `wpw_<weapon>_<target>=0-9` | Per-weapon priority |
| `glob_on=0` | cfg-only: unregister the whole priority feature |
| `glob_edit=1` | The priority pages write the global table (names say GLOBAL) |
| `targets_extra=0x…,…` | Extra lockable entity hashes |
| `debug=1` | WATCH lines every 120 frames + extra diagnostics |

Full reference: [manual](docs/README.md).

## Build

```powershell
python build.py
```

Python 3 only, no game or SDK needed. Produces
`Addon/9ba626afa44a3aa3.patch_0` and `Guided-Rounds-v1.9.12.zip`.
`--check-against` compares the output with BingusSharedLoader's reference
packer.

## Version

- **v1.9.12** — Voteless lock fix (dead cache only trusts `status=2`), zero-bone guard, WATCH counters
- **v1.9.11** — per-weapon priority reads the weapon in hand; CUSTOM also points the pages at that weapon; aim mode follows a weapon swap immediately; 0 = not set
- **v1.9.0** — weapon pages by class, priority pages by faction, Cognitive Disruptor hull removed, bilingual names
- **v1.8.6** — manual target priority, TARGET CENSUS, more Illuminate units
- **v1.8.5** — transports off by default, crash hardening
- **v1.8.3 / v1.8.4** — scope lock range matches hipfire
- **v1.8.1 / v1.8.2** — robustness and target-box cleanup

## License

See [`LICENSE`](LICENSE). Solo and private co-op only; follow the game's and the
community's rules.
