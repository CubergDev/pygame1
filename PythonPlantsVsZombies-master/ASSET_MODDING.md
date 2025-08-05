# Asset Replacement Pipeline

This guide walks through swapping the bundled art and audio with your own
creations.  Each section lists required formats, file names and, for
animations, the poses and frame counts the engine expects.

## Defenders

1. Prepare PNG frames for the defender's animation.
2. Drop them into `resources/graphics/Plants/<Folder>/` using the naming
   `<Folder>_0.png`, `<Folder>_1.png`, ...
3. If you change frame sizes or counts, update the rectangle data in
   `source/data/entity/plant.json`.
4. Optionally place `resources/sounds/<Hero>_deploy.ogg` and
   `resources/sounds/<Hero>_death.ogg` and load them in `source/tool.py`.

| Hero                | Asset folder(s)                                      | Frames | Poses                     |
|---------------------|------------------------------------------------------|-------:|---------------------------|
| SojuBottleSlingshot | `Peashooter`                                         |   13   | idle + shot               |
| EomukVendor         | `SunFlower`                                          |   18   | idle loop                 |
| SuitcaseBarricade   | `WallNut`, `WallNut_cracked1`, `WallNut_cracked2`    |   16   | intact and two cracked    |
| TaekwondoGuard      | `RepeaterPea`                                        |   15   | idle + shot               |
| MolotovStudent      | `CherryBomb`                                         |    7   | fuse to explosion         |
| KPopIdol            | `PuffShroom`, `PuffShroomSleep`                      | 14/17  | active loop / sleep       |

Cards that appear on the menubar live in `resources/graphics/Cards/` and
use the same PNG format.

## Start menu

1. Replace `resources/graphics/Screen/MainMenu.png` (PNG background).
2. Swap `Adventure_0.png` and `Adventure_1.png` for the start button's
   two animation frames.
3. If sizes change, tweak the rectangle values in
   `source/state/mainmenu.py`.
4. Optional menu music: load an `.ogg` in `Menu.startup` with
   `pygame.mixer.music`.

## Level backgrounds

1. Gameplay and UI panels reside in `resources/graphics/Screen/` as PNGs
   such as `ChooserBackground.png` or `PanelBackground.png`.
2. Replace these files with images of the same dimensions to reskin the
   play field and menus.

## Sun points

1. The pickup animation is stored under `resources/graphics/Plants/Sun/`
   as `Sun_0.png`–`Sun_21.png` (22 PNG frames).
2. Swap these frames to change the currency icon and adjust `SUN_VALUE`
   in `source/constants.py` if you want a different reward.

## Sounds

1. Store effects in `resources/sounds/` as `.ogg` or `.wav` files.
2. Use names like `<Hero>_deploy.ogg` and `<Hero>_death.ogg` for plants
   or `zombie_die.ogg` for enemies.
3. Load them in `source/tool.py`'s `SFX` dictionary and trigger with
   `SFX['name'].play()`.

## Effects and other animations

1. Aura, burn or custom effects live in
   `resources/graphics/Effects/<EffectName>/` as sequential PNG frames
   `<EffectName>_0.png`, `<EffectName>_1.png`, ...
2. Classes such as `MolotovFire` or `applyIdolBuffs` can be edited to
   adjust durations, radii or damage when introducing new effects.

## General tips

- Keep original filenames and folder structures to minimize code edits.
- PNG images should preserve transparency and match expected dimensions.
- Run `python -m py_compile` or `python -m compileall` after touching
  code to verify there are no syntax errors.

