# Guided Rounds — Manual

**English** | [简体中文](README.md) · [Project home](../README.md)

Guided Rounds gives every weapon in your arsenal the homing behaviour of the
**P-92 Warrant**. A round leaves the barrel, picks a target in the aim cone and
steers onto it — **damage, muzzle velocity and ballistics remain the weapon's
own values**.

- Authors: cancan2333 & SoS2430
- Version: 1.9.14
- Requires: Bingus Shared Loader v15+, Vanilla Plus Megapack. **HD2Runtime optional** (an installed one is preferred - its asset sync reaches clients without the loadout; the built-in loader takes over if it refuses)
- Source: `docs/guided_rounds.lua` · Build: `build.py`

## Install

1. Install the [HD2 Arsenal](https://www.nexusmods.com/helldivers2/mods/4664) loader.
2. Import `Guided-Rounds-v1.9.14.zip` in HD2 Arsenal, and install
   [Bingus Shared Loader](https://ayakamods.com/mods/bingus-shared-loader.3861/),
   [Vanilla Plus Megapack](https://www.nexusmods.com/helldivers2/mods/16294).
   [hd2runtime](https://ayakamods.com/mods/hd2runtime.4260/) is optional: an installed one
   is preferred (its lobby sync also reaches clients without the loadout); without it, or
   if it refuses, the built-in loader runs.
3. Load order, top to bottom: **Guided Rounds → Vanilla Plus Megapack → Bingus Shared Loader → hd2runtime** (drop the last line if hd2runtime is not installed).
4. Launch the game and open **Esc → MODS**.

The built-in loader requests the packages; the purple missing-material icon only
remains when the built-in loader does not recognise the game build and no
a usable HD2Runtime is installed.

## Menu map

The pack sorts category buttons by their first two digits, so the page numbers
are fixed:

| Page | Contents | Cap |
| --- | --- | ---: |
| `01 · GUIDED ROUNDS` | Master switch, 11 sliders, 16 toggles | 32 |
| `02 · GUIDED EXPLOSIVE FUSE` | 4 fuse sliders | 32 |
| `03–11 · GUIDED <CLASS>` | 9 weapon classes, 4 options per weapon | 32/page |
| `12 · GUIDED WEAPON PRIORITY` | Pick the weapon whose table pages 13+ edit | 31 |
| `13 · GUIDED TARGET PRIORITY` | Manual priority master switch | 32 |
| `14+ · GUIDED TERMINIDS` | Terminids, 32 per page | 32 |
| `14+ · GUIDED AUTOMATONS` | Automatons, 32 per page | 32 |
| `14+ · GUIDED ILLUMINATE` | Illuminate | 32 |
| `14+ · GUIDED OTHER TARGETS` | Vehicles, structures, the rest | 32 |

Weapon classes: assault rifles, explosive, marksman rifles, submachine guns,
shotguns, support weapons, energy weapons, special weapons, pistols. Support
weapons always land on the support page. Names follow the game language.

### Pages 03–11: four options per weapon

| Option | Effect |
| --- | --- |
| `OFF` | This weapon is not guided |
| `AIM FIRST` | Guided, target nearest the crosshair |
| `BIGGEST HP FIRST` | Guided, biggest health first |
| `SMALLEST HP FIRST` | Guided, smallest health first |

The first two write `weapons=`, the last two `prio_targets=` / `prio_small=`.

### Page 12: per-weapon priority

Lists the weapons that are already locked on, by class (`wpcls`). Each row has
three states:

- `OFF` — switch that weapon's own table off (`wpc_<weapon>=0`). If it is the
  current edit target, the edit target is cleared too.
- `CUSTOM` — switch that weapon's own table on **and point pages 13–19 at it**.
- `EDIT` — same, plus the row keeps a `*` marker for this menu session.

Both `CUSTOM` and `EDIT` force `glob_edit=0`; otherwise the priority pages write
the global table.

## Page 01 — main settings

| Slider | Key | Range | Default | Effect |
| --- | --- | ---: | ---: | --- |
| LOCK ANGLE (deg) | `cone_deg` | 0–60 | 12 | Degrees off the barrel a target may sit; 0 draws no ring |
| LOCK RANGE (m) | `max_dist` | 0–500 | 250 | Furthest lock range |
| ARM TIME AFTER MUZZLE (s) | `bind_delay` | 0–2 | 0.25 | How long after the muzzle a binding is allowed |
| SCOPE LOCK SCALE | `scope_scale` | 0.05–1 | 0.3 | Only used with FOLLOW THE SCOPE ZOOM |
| TARGET REFRESH (frames) | `target_interval` | 1–60 | 20 | How often the target list is rebuilt |
| BALLISTICS ROW SPEED (mps) | `round_speed` | 0–2000 | 0 | Solid-ammo muzzle speed, 0 = leave it |
| BALLISTICS ROW GRAVITY | `round_gravity` | -1–3 | -1 | Gravity multiplier, -1 = leave it |
| BOMBLET ARM TIME (s) | `cluster_delay` | 0–1 | 0.05 | Delay before a bomblet accepts a target |
| BOMBLET SEEKER (0–7) | `cluster_seeker` | 0–7 | 1 | Seeker entity the bomblets borrow |
| ROCKET SEEKER (0–9) | `launcher_seeker` | 0–9 | 0 | Seeker entity the cluster rocket borrows |
| GUIDED DARTS PER SHOT | `swarm_count` | 0–64 | 25 | ≥2 turns CLUSTER into a guided swarm |

Seeker entities 0–7: 0 = P-92 Warrant (TargetLock, needs a weapon lock),
1 = MLS-4X commando missile, 2 = Patriot exosuit rocket, 3 = Mini Missile Silo
missile, 4 = plain Guidance, 5 = enemy homing rocket, 6 = fast Behaviour seeker,
7 = Vox Engine (waits for the target this addon publishes). `launcher_seeker`
also accepts 8 = P-33 round, 9 = FAF-14 Spear.

### Toggles

| Toggle | Key | Default | Effect |
| --- | --- | ---: | --- |
| RANGE RING | `range_ring` | 1 | Aim-cone ring around the crosshair |
| LOCK MARKERS | `lock_reticle` | 1 | Stock lock markers |
| TARGET BOX | `target_box` | 1 | Wire box around the locked target |
| LOCK HELLDIVERS ONLY | `lock_helldivers` | 0 | Lock teammates instead of enemies |
| LOCK ILLUMINATE WARPSHIPS | `lock_shuttle` | 0 | Allow the Warp Ship and its shield |
| LOCK AUTOMATON DROPSHIPS | `lock_dropship` | 0 | Allow the Automaton Dropship |
| ONLY GUIDE THE FLAK ROUND | `flak_only` | 1 | Cluster stays stock, only flak is guided |
| BIND TARGET OURSELVES | `lua_bind` | 1 | Bind a target when the engine did not |
| REQUIRES LINE OF SIGHT | `los_check` | 1 | Refuse targets behind cover |
| SHOOT THROUGH FOLIAGE | `los_foliage` | 1 | Leaves do not block the lock |
| NEAREST ENEMY FALLBACK | `cone_fallback` | 0 | With an empty cone, take the nearest enemy |
| GUIDE RL-77 CLUSTER BOMBLETS | `cluster_guide` | 1 | Guide the RL-77 bomblets |
| KEEP THE WEAPON OWN DAMAGE | `apw_damage` | 1 | Restore the weapon's own damage |
| LOAD PROJECTILE MATERIALS | `require_assets` | 1 | Keep the projectile material loaded (HD2Runtime preferred when installed, built-in loader otherwise) |
| FOLLOW THE SCOPE ZOOM | `scope_fix` | 0 | Lock range follows scope magnification |
| ENABLE | `enable` | 1 | Master switch (F7 restarts it) |

## Page 02 — explosive fuse

| Slider | Key | Range | Default | Effect |
| --- | --- | ---: | ---: | --- |
| ROUND FUSE TIME (s) | `round_life` | 0–15 | 0 | Self-destruct timer, 0 = leave it |
| CLUSTER BOMBLET LIFE (s) | `cluster_life` | 0.1–8 | 3 | Bomblet lifetime; factory 0 means never expire |
| CLUSTER AIRBURST DELAY (s) | `rocket_life` | 0–5 | 1.5 | Time before the cluster round bursts; factory 0.25 |
| CLUSTER PROXIMITY FUSE (m) | `rocket_prox` | 0–20 | 0 | Add a proximity fuse, 0 = off |

## Three layers of target priority

When a target is chosen the priority number decides first (lower wins); only
ties are broken by the weapon's aim mode (crosshair / biggest / smallest).

### Layer 1 — aim mode per weapon (pages 03–11)

The coarse four-way choice described above. No table of its own.

### Layer 2 — global table (pages 13–19)

Enabled by `prio_manual=1`. One 0–9 slider per target: **1 locks first, 9 last,
0 = not set**. Stored as `tp_<16 hex target>=<n>`. Targets the pages do not list
can still be added by hand.

### Layer 3 — per-weapon table (page 12 + pages 13–19)

This is the part v1.9.11 fixed:

1. On page 12 find the weapon and pick `CUSTOM` (or `EDIT`). The addon records
   it as the edit target (`wprio_sel=0x<weapon>`, `wpc_<weapon>=1`) and clears
   `glob_edit`.
2. Go to pages 13–19 and drag the sliders. This writes
   **`wpw_<weapon>_<target>=<n>`**, and the page title shows the weapon name.
3. Switch weapons: return to page 12, pick the other weapon's `CUSTOM`, drag
   again. `wpw_` rows are per weapon and never collide.

Rules:

- **0 = not set**: dragging to 0 inside the weapon's table falls back to the
  global `tp_` when locking. Only when both layers are 0 is there no priority at
  all and the aim mode decides.
- The table only affects the **weapon in hand** — the one the crosshair points
  at, not the one on your back.
- Turning a weapon's `CUSTOM` off (`OFF`) makes it use the global table again;
  its `wpw_` rows are kept.
- With `glob_edit=1` pages 13–19 write the global `tp_` table again (titles say
  GLOBAL); the per-weapon tables still exist.

## cfg reference

Path: `%LOCALAPPDATA%\Hd2ApwGuidance\apw_guidance.cfg`. The menu writes it; by
hand, edit it with the game closed, one `key=value` per line.

| Key | Default | Meaning |
| --- | --- | --- |
| `cfgver` | 16 | Config version; on mismatch the old file is renamed `.v<ver>.bak` and defaults are written |
| `enable` | 1 | Master switch |
| `autostart` | 1 | Arm automatically on game start |
| `key` | 118 | F7: restart (put everything back, then take over again) |
| `weapons` | `0x89C5493E08CA4207` | Guided weapon list (comma separated) |
| `prio_targets` / `prio_small` | empty | Weapons that prefer biggest / smallest |
| `prio_manual` | 0 | Manual priority master switch |
| `tp_<16 hex>` | none | Global target priority 0–9 |
| `wpc_<16 hex weapon>` | none | 1 = use that weapon's own table |
| `wpw_<weapon>_<target>` | none | Per-weapon priority 0–9 |
| `wprio_sel` | `0x0` | Weapon whose table pages 13–19 edit (`0x` + 16 hex) |
| `wpcls` | 1 | Weapon class listed on page 12, 1–9 |
| `glob_on` | 1 | 0 = the whole priority feature is unregistered (only the 03–11 aim modes remain) |
| `glob_edit` | 0 | 1 = priority pages write the global table |
| `targets_extra` | empty | Extra lockable entity hashes, comma separated |
| `targets_debug` | 0 | 1 = log unnamed entities (TARGET CENSUS) |
| `debug` | 0 | 1 = WATCH line every 120 frames |
| `los_debug` | 0 | 1 = line-of-sight diagnostics |
| `los_desc` | 0 | Descriptor index used by the line-of-sight test |
| `scan_ms` | 1.5 | Memory scan milliseconds per frame while locating data |
| `cluster_guide` | 1 | Guide RL-77 bomblets |
| `cluster_life` | 3 | Bomblet lifetime |
| `cluster_delay` | 0.05 | Bomblet binding delay |
| `cluster_seeker` | 1 | Bomblet seeker 0–7 |
| `cluster_autofix` | 1 | Upgrade the never-homing 0 to 1 |
| `launcher_seeker` | 0 | Rocket seeker 0–9 |
| `rocket_life` | 1.5 | Cluster burst delay |
| `rocket_prox` | 0 | Cluster proximity fuse |
| `swarm_count` | 25 | Guided darts per shot; 0/1 keeps the airburst |
| `swarm_split` | 1 | Each dart picks its own target |

## Troubleshooting

**Nothing locks**: check `enable=1`, press F7, verify the load order and that
`require_assets` is still on; then check whether `cone_deg` / `max_dist` /
`los_check` filter the target out.

**One particular body will not lock** (what v1.9.12 fixed): set `debug=1`, play a
match and read the log:

```
WATCH <name> seen=.. wanted=.. health=.. dead=.. status=.. faction=.. pose=.. usable=..
```

- `dead` rising: the dead cache holds the unit (it only trusts `status=2`; if it
  still happens, there is a new status value).
- `status` rising: a live body reporting `status≠0` (a second record such as the
  decaying constitution value).
- `health` not rising: whitelist or health gate.
- `wanted` rises but `usable` does not: the pose bone cannot be read.

`targets_debug=1` logs `TARGET CENSUS res= hp= max= status= mask= pose_node= flags= unit= listed= in_list=` for unnamed entities; take `res` and add it to
`targets_extra`.

**The v1.9.12 Voteless case**: a Voteless carries a second record for its
decaying constitution value that reports `status=1` while the body is alive. The
old rule treated any non-zero status as death and dropped the whole unit for
3600 frames, repeatedly. The cache now only accepts `status=2`, and a body-part
row can no longer condemn the body.

**Rounds are purple question marks**: `require_assets=0`, or the built-in loader does
not recognise this game build while no usable HD2Runtime is installed, or
`require_assets=0`.

**Ring size looks wrong**: with `scope_fix=0` the ring keeps the same screen size
at every zoom; with it on, it scales by `scope_scale`.

## Build and checks

```powershell
python build.py              # Addon + zip
python build.py --check-against "../BingusSharedLoader-source-v19"
```

Outputs `Addon/9ba626afa44a3aa3.patch_0` and `Guided-Rounds-v1.9.14.zip`.
`tools/` holds read-only checkers (syntax, globals, locals, package layout,
persistence); see `tools/README.md` for their path requirements.

## Version history

| Version | Change |
| --- | --- |
| v1.9.14 | Fixes the pink question mark clients saw with v1.9.13: the built-in loader waits for the game to start before proving/requesting, boot-time failures no longer disable it for the session; an installed HD2Runtime is preferred and the built-in loader is the fallback |
| v1.9.12 | Voteless lock fix: dead cache only trusts `status=2`; zero bone treated as unreadable; WATCH gains `dead=`/`status=` |
| v1.9.11 | Per-weapon priority reads the weapon the crosshair points at; `CUSTOM` also points the pages at it and clears `glob_edit`; aim mode follows a weapon swap at once; `0 = not set` |
| v1.9.10 | Priority edit target survives menu closes; page 12 is three-state |
| v1.9.9 | Priority sliders show the per-weapon value |
| v1.9.8 | Dead cache, more Illuminate units, debug switches |
| v1.9.5 | Numeric page prefixes, fixed page sorting |
| v1.9.2 | Per-weapon priority introduced |
| v1.9.0 | Weapon pages by class, priority pages by faction, Cognitive Disruptor hull removed, bilingual names |
| v1.8.6 | Manual target priority, TARGET CENSUS, more Illuminate units |
| v1.8.5 | Transports off by default, crash hardening |
| v1.8.3 / v1.8.4 | Scope lock range matches hipfire; magnification follows |
| v1.8.1 / v1.8.2 | Robustness, target-box cleanup |

## License

See [LICENSE](../LICENSE). Solo and private co-op only; follow the game's and the
community's rules.
