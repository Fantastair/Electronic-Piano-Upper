import fantas
from fantas import uimanager as u

from style import *

import piano

root = fantas.Root(None)
fantas.Label((u.WIDTH, u.HEIGHT // 2), bg=LIGHTBROWN, topleft=(0, u.HEIGHT // 2)).join(u.root)
fantas.Label((u.WIDTH, 8), bg=DEEPBLUE, midleft=(0, u.HEIGHT // 2)).join(u.root)

for i in range(8):
    piano.PianoKey(midtop=(113 + 82 * i, u.HEIGHT // 2 - 4)).join(u.root)
