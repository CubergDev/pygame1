# Asset Replacement Pipeline

This guide walks through swapping the bundled art and audio with your own

creations. Every asset lives under `resources/` and is loaded purely by
its filename, so replacing a file with one that uses the exact same name
is enough for the game to pick it up. The sections below list the folders,
exact file names, expected frame counts and optional sounds for each
defender plus the surrounding UI.

## Defenders

For every defender place PNG frames in the folders listed below. Filenames
must be zero‑indexed and consecutive (`Foo_0.png`, `Foo_1.png`, …). The
engine uses whatever size you supply, but if you change dimensions or
frame counts update the matching rectangle entry in
`source/data/entity/plant.json`.

### SojuBottleSlingshot (Peashooter)
* **Sprite folder:** `resources/graphics/Plants/Peashooter/`
* **Frames:** 13 files `Peashooter_0.png` … `Peashooter_12.png`
* **Card art:** `resources/graphics/Cards/card_peashooter.png` and
  `card_peashooter_move.png`
* **Bullet:** replace `resources/graphics/Bullets/PeaNormal/PeaNormal_0.png`
  and `resources/graphics/Bullets/PeaNormalExplode/PeaNormalExplode_0.png`
* **Optional sounds:** `resources/sounds/SojuBottleSlingshot_deploy.ogg` and
  `SojuBottleSlingshot_death.ogg`

### EomukVendor (SunFlower)
* **Sprite folder:** `resources/graphics/Plants/SunFlower/`
* **Frames:** 18 files `SunFlower_0.png` … `SunFlower_17.png`
* **Card art:** `resources/graphics/Cards/card_sunflower.png` and
  `card_sunflower_move.png`
* **Optional sounds:** `resources/sounds/EomukVendor_deploy.ogg` and
  `EomukVendor_death.ogg`

### SuitcaseBarricade (WallNut)
* **Sprite folders:**
  * `resources/graphics/Plants/WallNut/WallNut/` – 16 files
    `WallNut_0.png` … `WallNut_15.png` (intact)
  * `resources/graphics/Plants/WallNut/WallNut_cracked1/` – 11 files
    `WallNut_cracked1_0.png` … `WallNut_cracked1_10.png`
  * `resources/graphics/Plants/WallNut/WallNut_cracked2/` – 15 files
    `WallNut_cracked2_0.png` … `WallNut_cracked2_14.png`
* **Card art:** `resources/graphics/Cards/card_wallnut.png` and
  `card_wallnut_move.png`
* **Optional sounds:** `resources/sounds/SuitcaseBarricade_deploy.ogg` and
  `SuitcaseBarricade_death.ogg`

### TaekwondoGuard (RepeaterPea)
* **Sprite folder:** `resources/graphics/Plants/RepeaterPea/`
* **Frames:** 15 files `RepeaterPea_0.png` … `RepeaterPea_14.png`
* **Card art:** `resources/graphics/Cards/card_repeaterpea.png` and
  `card_repeaterpea_move.png`
* **Bullet:** uses the same pea assets as SojuBottleSlingshot
* **Optional sounds:** `resources/sounds/TaekwondoGuard_deploy.ogg` and
  `TaekwondoGuard_death.ogg`

### MolotovStudent (CherryBomb)
* **Sprite folder:** `resources/graphics/Plants/CherryBomb/`
* **Frames:** 7 files `CherryBomb_0.png` … `CherryBomb_6.png`
* **Card art:** `resources/graphics/Cards/card_cherrybomb.png` and
  `card_cherrybomb_move.png`

* **Projectile:** optional frames in
  `resources/graphics/Effects/MolotovProjectile/MolotovProjectile_0.png`,
  `MolotovProjectile_1.png`, …

* **Burn effect:** supply frames in
  `resources/graphics/Effects/MolotovFire/MolotovFire_0.png`,
  `MolotovFire_1.png`, … as desired
* **Optional sounds:** `resources/sounds/MolotovStudent_deploy.ogg` and
  `MolotovStudent_death.ogg`

### KPopIdol (PuffShroom)
* **Sprite folders:**
  * Active: `resources/graphics/Plants/PuffShroom/PuffShroom/` – 14 files
    `PuffShroom_0.png` … `PuffShroom_13.png`
  * Sleeping: `resources/graphics/Plants/PuffShroom/PuffShroomSleep/` – 17
    files `PuffShroomSleep_0.png` … `PuffShroomSleep_16.png`
* **Card art:** `resources/graphics/Cards/card_puffshroom.png` and
  `card_puffshroom_move.png`
* **Aura effect:** optional frames in
  `resources/graphics/Effects/KPopAura/KPopAura_0.png`, …
* **Optional sounds:** `resources/sounds/KPopIdol_deploy.ogg` and
  `KPopIdol_death.ogg`

Cards for all defenders must remain in `resources/graphics/Cards/` and keep
their original `card_<plant>.png` and `card_<plant>_move.png` names so the
menubar finds them.


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

