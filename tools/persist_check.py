"""End-to-end persistence check for the two priority layers.

Stage 1 seeds a cfg, loads the addon through the game's own lua51.dll, drives
the real menu handlers (the ones that call state.save_cfg_key) and reads the
cfg file back.
Stage 2 loads the same cfg in a fresh Lua state - every number must return.

Run: python tools/persist_check.py   (expect "persistence: PASS")
"""
import io
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / 'docs' / 'guided_rounds.lua'
SCRATCH = ROOT / '.persist'
CFGDIR = SCRATCH / 'Hd2ApwGuidance'
CFG = CFGDIR / 'apw_guidance.cfg'
TMP = SCRATCH / 'tmp_persist.lua'

sys.path.insert(0, str(HERE))
import loadtest  # noqa: E402

W = '7F76685519F2AFB6'          # R-36 Eruptor, reversed spelling
T = 'DF974365BBD89CF7'          # Alpha Commander

SEED = """cfgver=1
weapons=0xB6AFF2195568767F
prio_manual=1
glob_on=1
glob_edit=0
wpc_@W@=1
wprio_sel=0x@W@
wpcls=9
tp_@T@=4
wpw_@W@_@T@=2
""".replace('@W@', W).replace('@T@', T)

PROBE1 = r'''
for i = 1, 3 do update() end
local M = rawget(_G, 'ModOptionsMenu')
local P = rawget(_G, '__pcfg')
local S = rawget(_G, '__pstate')
local TW, TT = '@W@', '@T@'
local tp_id, wpw_id, wpc_id = 'tp_' .. TT, 'wpw_' .. TW .. '_' .. TT, 'wpc_' .. TW
local out = {}
local function add(s) out[#out + 1] = s end
add('LOADED tp=' .. tostring(P[tp_id]) .. ' wpw=' .. tostring(P[wpw_id])
    .. ' wpc=' .. tostring(P[wpc_id]) .. ' prio=' .. tostring(P.prio_manual)
    .. ' glob_edit=' .. tostring(P.glob_edit) .. ' sel=' .. tostring(S.wprio_sel)
    .. ' wpcls=' .. tostring(S.wpcls_want))
local slot = M.options['apw_wpslot_1']
if slot and type(slot.label) == 'function' then slot.label() end
if M.changes['apw_wpslot_1'] then M.changes['apw_wpslot_1'](3) end
local id
for _, v in ipairs(M.order) do
    if v == 'apw_tp_' .. TT then id = v end
end
add('ROW ' .. tostring(id))
if M.changes[id] then M.changes[id](6) end
if M.changes['apw_prio_manual'] then M.changes['apw_prio_manual'](false) end
if M.changes[id] then M.changes[id](8) end
if M.changes['apw_wpcls'] then M.changes['apw_wpcls'](3) end
add('AFTER tp=' .. tostring(P[tp_id]) .. ' wpw=' .. tostring(P[wpw_id])
    .. ' prio=' .. tostring(P.prio_manual) .. ' glob_edit=' .. tostring(P.glob_edit)
    .. ' sel=' .. tostring(S.wprio_sel) .. ' wpcls=' .. tostring(S.wpcls_want))
return table.concat(out, ' | ')
'''.replace('@W@', W).replace('@T@', T)

PROBE2 = r'''
for i = 1, 3 do update() end
local M = rawget(_G, 'ModOptionsMenu')
local P = rawget(_G, '__pcfg')
local S = rawget(_G, '__pstate')
local TW, TT = '@W@', '@T@'
local slot = M.options['apw_wpslot_1']
if slot and type(slot.label) == 'function' then slot.label() end
for i = 1, 3 do update() end
return 'RELOADED tp=' .. tostring(P['tp_' .. TT])
    .. ' wpw=' .. tostring(P['wpw_' .. TW .. '_' .. TT])
    .. ' wpc=' .. tostring(P['wpc_' .. TW])
    .. ' prio=' .. tostring(P.prio_manual)
    .. ' glob_edit=' .. tostring(P.glob_edit)
    .. ' sel=' .. tostring(S.wprio_sel)
    .. ' wpcls=' .. tostring(S.wpcls_want)
    .. ' row_tp=' .. tostring(M.get('apw_tp_' .. TT))
    .. ' row_slot=' .. tostring(M.get('apw_wpslot_1'))
'''.replace('@W@', W).replace('@T@', T)


SEED_EDIT = """cfgver=16
weapons=0xB6AFF2195568767F
prio_manual=0
glob_on=1
glob_edit=1
wpcls=9
"""

PROBE3 = r'''
for i = 1, 3 do update() end
local M = rawget(_G, 'ModOptionsMenu')
local S = rawget(_G, '__pstate')
local C = rawget(_G, '__pcfg')
S.wpcls_want = 9
local out = {}
local function add(s) out[#out + 1] = s end
M.options['apw_wpslot_1'].label()
for i = 1, 3 do update() end
M.changes['apw_wpslot_1'](3)
for i = 1, 3 do update() end
add('after EDIT row=' .. tostring(M.get('apw_wpslot_1'))
    .. ' sel=' .. tostring(S.wprio_sel) .. ' wp_edit=' .. tostring(S.wp_edit))
M.options['apw_wpslot_1'].label()      -- the pack resolves it once per menu open
for i = 1, 3 do update() end
add('next open row=' .. tostring(M.get('apw_wpslot_1'))
    .. ' wp_edit=' .. tostring(S.wp_edit))
M.changes['apw_glob_edit'](false)      -- manual layer off: must refuse
for i = 1, 3 do update() end
add('manual off, glob_edit off -> cfg=' .. tostring(C.glob_edit)
    .. ' row=' .. tostring(M.get('apw_glob_edit')))
M.changes['apw_prio_manual'](true)
for i = 1, 3 do update() end
M.changes['apw_glob_edit'](false)      -- manual layer on: allowed again
for i = 1, 3 do update() end
add('manual on, glob_edit off -> cfg=' .. tostring(C.glob_edit)
    .. ' row=' .. tostring(M.get('apw_glob_edit')))
return table.concat(out, ' | ')
'''


def patched_source():
    t = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    anchor = '\nctx = {'
    assert t.count(anchor) == 1
    t = t.replace(anchor, "\nrawset(_G, '__pcfg', cfg)\nrawset(_G, '__pstate', state)\n" + anchor)
    io.open(TMP, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
    return t


def run(probe, label):
    src = patched_source()
    status, msg = loadtest.run(src.encode('utf-8'), probe,
                               (loadtest.PRELUDE + loadtest.MENU_STUB).encode('utf-8'))
    print(' ', label, 'status', status, '|', msg[:400])
    assert status == 0, msg
    return msg


def key(text, name):
    for line in text.splitlines():
        if line.strip().startswith(name + '='):
            return line.strip().split('=', 1)[1]
    return None


def count_prefix(text, prefix):
    return sum(1 for line in text.splitlines() if line.startswith(prefix))


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    CFGDIR.mkdir(parents=True, exist_ok=True)
    io.open(CFG, 'w', encoding='utf-8', newline='').write(SEED)
    os.environ['LOCALAPPDATA'] = str(SCRATCH)

    print('stage 1 - load the seed, drive the handlers, write the cfg')
    run(PROBE1, 's1')
    text = io.open(CFG, encoding='utf-8', newline='').read()
    checks = [
        ('tp_' + T, '8'), ('wpw_' + W + '_' + T, '6'), ('wpc_' + W, '1'),
        ('prio_manual', '0'), ('glob_edit', '1'), ('wpcls', '3'),
        ('wprio_sel', '0x' + W),
    ]
    for name, want in checks:
        got = key(text, name)
        print(f'  {name:36s} {str(got)!r:20s} want {want!r}',
              'ok' if got == want else 'MISMATCH')
        assert got == want, (name, got, want)
    # a menu open must not invent a line for every untouched target
    assert count_prefix(text, 'tp_') == 1, count_prefix(text, 'tp_')

    print('stage 2 - fresh state, same cfg')
    msg = run(PROBE2, 's2')
    assert 'row_tp=8' in msg, msg

    print('stage 3 - menu behaviour (EDIT is momentary across a menu cycle)')
    io.open(CFG, 'w', encoding='utf-8', newline='').write(SEED_EDIT)
    msg = run(PROBE3, 's3')
    for want in ('after EDIT row=3', 'next open row=2',
                 'manual off, glob_edit off -> cfg=1 row=true',
                 'manual on, glob_edit off -> cfg=0 row=false'):
        print('  want', repr(want), 'ok' if want in msg else 'MISSING')
        assert want in msg, (want, msg)

    TMP.unlink(missing_ok=True)
    print('persistence: PASS')


if __name__ == '__main__':
    main()
