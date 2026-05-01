#!/usr/bin/env python3
"""Generate placeholder PNG sprites for all WH40K mod units and buildings.

Run from the repo root:
    python3 tools/generate_sprites.py
"""

import struct
import zlib
import os

FACTION_COLORS = {
    'space_marines': (26, 75, 140),
    'orks':          (45, 107, 45),
    'necrons':       (160, 168, 176),
    'chaos':         (139, 26, 26),
    'shared':        (180, 160, 60),   # gold — neutral faction selector
}
DESTROYED_COLOR = (85, 85, 85)
MK2_TINT = 40  # added to each channel for Mk2 upgrade sprites


def _darker(color, factor=0.65):
    return tuple(max(0, int(c * factor)) for c in color)


def _lighter(color, amount=MK2_TINT):
    return tuple(min(255, c + amount) for c in color)


def make_png(width, height, fill, border_color=None, border_w=2):
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            on_border = border_color and (
                x < border_w or x >= width - border_w or
                y < border_w or y >= height - border_w
            )
            r, g, b = border_color if on_border else fill
            row += bytes([r, g, b])
        rows.append(b'\x00' + bytes(row))

    raw = b''.join(rows)
    compressed = zlib.compress(raw, 9)

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', compressed)
        + chunk(b'IEND', b'')
    )


def write_png(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


# (faction_dir, prefix, slug, is_large)
# is_large=True  → 48×48 sprite (buildings + mega vehicles)
# is_large=False → 32×32 sprite (standard units)
# slug ending in '_mk2' gets a lighter tint on its base sprite
MANIFEST = [
    # ── Space Marines ──────────────────────────────────────────
    ('space_marines', 'sm', 'techmarine',      False),
    ('space_marines', 'sm', 'scout',           False),
    ('space_marines', 'sm', 'tactical',        False),
    ('space_marines', 'sm', 'assault',         False),
    ('space_marines', 'sm', 'devastator',      False),
    ('space_marines', 'sm', 'terminator',      False),
    ('space_marines', 'sm', 'apothecary',      False),
    ('space_marines', 'sm', 'land_speeder',    False),
    ('space_marines', 'sm', 'rhino',           False),
    ('space_marines', 'sm', 'dreadnought',     False),
    ('space_marines', 'sm', 'predator',        False),
    ('space_marines', 'sm', 'land_raider',     False),
    ('space_marines', 'sm', 'thunderhawk',     False),
    ('space_marines', 'sm', 'captain',         False),
    ('space_marines', 'sm', 'hq',              True),
    ('space_marines', 'sm', 'barracks',        True),
    ('space_marines', 'sm', 'factory',         True),
    ('space_marines', 'sm', 'airfield',        True),
    ('space_marines', 'sm', 'turret',          True),
    ('space_marines', 'sm', 'at_turret',       True),
    ('space_marines', 'sm', 'at_turret_mk2',   True),
    ('space_marines', 'sm', 'aa_turret',       True),
    ('space_marines', 'sm', 'aa_turret_mk2',   True),
    ('space_marines', 'sm', 'generator',       True),
    ('space_marines', 'sm', 'wall',            True),
    ('space_marines', 'sm', 'warlord_titan',   True),
    # ── Orks ───────────────────────────────────────────────────
    ('orks', 'ork', 'mek_boy',        False),
    ('orks', 'ork', 'gretchin',       False),
    ('orks', 'ork', 'boyz',           False),
    ('orks', 'ork', 'burna_boyz',     False),
    ('orks', 'ork', 'nobz',           False),
    ('orks', 'ork', 'lootas',         False),
    ('orks', 'ork', 'painboy',        False),
    ('orks', 'ork', 'warbiker',       False),
    ('orks', 'ork', 'trukk',          False),
    ('orks', 'ork', 'deff_dread',     False),
    ('orks', 'ork', 'battlewagon',    False),
    ('orks', 'ork', 'stompa',         False),
    ('orks', 'ork', 'dakkjet',        False),
    ('orks', 'ork', 'warboss',        False),
    ('orks', 'ork', 'hq',             True),
    ('orks', 'ork', 'barracks',       True),
    ('orks', 'ork', 'factory',        True),
    ('orks', 'ork', 'airfield',       True),
    ('orks', 'ork', 'turret',         True),
    ('orks', 'ork', 'at_turret',      True),
    ('orks', 'ork', 'at_turret_mk2',  True),
    ('orks', 'ork', 'aa_turret',      True),
    ('orks', 'ork', 'aa_turret_mk2',  True),
    ('orks', 'ork', 'generator',      True),
    ('orks', 'ork', 'wall',           True),
    ('orks', 'ork', 'gargant',        True),
    # ── Necrons ────────────────────────────────────────────────
    ('necrons', 'nec', 'cryptek',             False),
    ('necrons', 'nec', 'warriors',            False),
    ('necrons', 'nec', 'immortals',           False),
    ('necrons', 'nec', 'flayed_ones',         False),
    ('necrons', 'nec', 'deathmarks',          False),
    ('necrons', 'nec', 'lychguard',           False),
    ('necrons', 'nec', 'scarabs',             False),
    ('necrons', 'nec', 'wraiths',             False),
    ('necrons', 'nec', 'canoptek_spyder',     False),
    ('necrons', 'nec', 'ghost_ark',           False),
    ('necrons', 'nec', 'annihilation_barge',  False),
    ('necrons', 'nec', 'doomsday_ark',        False),
    ('necrons', 'nec', 'monolith',            False),
    ('necrons', 'nec', 'overlord',            False),
    ('necrons', 'nec', 'hq',                  True),
    ('necrons', 'nec', 'barracks',            True),
    ('necrons', 'nec', 'factory',             True),
    ('necrons', 'nec', 'airfield',            True),
    ('necrons', 'nec', 'turret',              True),
    ('necrons', 'nec', 'at_turret',           True),
    ('necrons', 'nec', 'at_turret_mk2',       True),
    ('necrons', 'nec', 'aa_turret',           True),
    ('necrons', 'nec', 'aa_turret_mk2',       True),
    ('necrons', 'nec', 'generator',           True),
    ('necrons', 'nec', 'wall',                True),
    ('necrons', 'nec', 'tesseract_vault',     True),
    # ── Shared ─────────────────────────────────────────────────
    ('shared', 'wh40k', 'selector', True),
    # ── Chaos Space Marines ────────────────────────────────────
    ('chaos', 'csm', 'warpsmith',       False),
    ('chaos', 'csm', 'cultists',        False),
    ('chaos', 'csm', 'chaos_marines',   False),
    ('chaos', 'csm', 'berzerkers',      False),
    ('chaos', 'csm', 'plague_marines',  False),
    ('chaos', 'csm', 'terminators',     False),
    ('chaos', 'csm', 'obliterators',    False),
    ('chaos', 'csm', 'dark_apostle',    False),
    ('chaos', 'csm', 'rhino',           False),
    ('chaos', 'csm', 'predator',        False),
    ('chaos', 'csm', 'defiler',         False),
    ('chaos', 'csm', 'heldrake',        False),
    ('chaos', 'csm', 'land_raider',     False),
    ('chaos', 'csm', 'chaos_lord',      False),
    ('chaos', 'csm', 'hq',              True),
    ('chaos', 'csm', 'barracks',        True),
    ('chaos', 'csm', 'factory',         True),
    ('chaos', 'csm', 'airfield',        True),
    ('chaos', 'csm', 'turret',          True),
    ('chaos', 'csm', 'at_turret',       True),
    ('chaos', 'csm', 'at_turret_mk2',   True),
    ('chaos', 'csm', 'aa_turret',       True),
    ('chaos', 'csm', 'aa_turret_mk2',   True),
    ('chaos', 'csm', 'generator',       True),
    ('chaos', 'csm', 'wall',            True),
    ('chaos', 'csm', 'brass_scorpion',  True),
]


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generated = 0

    for faction_dir, prefix, slug, is_large in MANIFEST:
        color = FACTION_COLORS[faction_dir]
        size = 48 if is_large else 32
        border_w = 4 if is_large else 2

        fill = _lighter(color) if slug.endswith('_mk2') else color
        border = _darker(fill)
        destroyed_border = _darker(DESTROYED_COLOR)

        base_png = make_png(size, size, fill, border, border_w)
        dest_png = make_png(size, size, DESTROYED_COLOR, destroyed_border, border_w)

        sprite_dir = os.path.join(base_dir, 'sprites', faction_dir)
        write_png(os.path.join(sprite_dir, f'{prefix}_{slug}_base.png'), base_png)
        write_png(os.path.join(sprite_dir, f'{prefix}_{slug}_destroyed.png'), dest_png)
        generated += 2

    print(f'Generated {generated} sprite PNGs across {len(MANIFEST)} entries.')


if __name__ == '__main__':
    main()
