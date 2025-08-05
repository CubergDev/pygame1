# Asset Customization Guide

This project loads most of its visuals from the `resources/graphics` folder and can be extended with sound and music through `pygame.mixer`.  The following sections describe how to replace common game assets.

## Plant sprites
1. Each plant has a sub‑folder under `resources/graphics/Plants/` (for example, `Peashooter`, `WallNut`, `SunFlower`).
2. Inside each folder, animation frames are named `<PlantName>_0.png`, `<PlantName>_1.png`, etc.  Replace these files with your own PNGs while keeping the same naming scheme.
3. If you add or remove frames, update the `plant.json` rectangle definitions in `source/data/entity/plant.json` to match the new frame sizes.
4. Card thumbnails live in `resources/graphics/Cards/`; swap these images to change the icons shown on the menubar.

## Backgrounds
1. Gameplay backgrounds and UI panels are located in `resources/graphics/Screen/`.  Files such as `Adventure_0.png`, `ChooserBackground.png`, and `PanelBackground.png` correspond to level fields and menus.
2. Replace any background image with another of the same dimensions to change the in‑game scenery.

## Sounds and music
1. Create `resources/sounds/` for effects and `resources/music/` for loops.  Store audio as `.ogg` or `.wav`.
2. In `source/tool.py`, load the audio with `pygame.mixer.Sound` for effects or `pygame.mixer.music.load` for background tracks:
   ```python
   SFX = {
       'plant': pg.mixer.Sound('resources/sounds/plant.ogg'),
       'zombie': pg.mixer.Sound('resources/sounds/zombie.ogg')
   }
   pg.mixer.music.load('resources/music/theme.ogg')
   pg.mixer.music.play(-1)
   ```
3. Play the effects from gameplay code, e.g. `SFX['plant'].play()` when a plant is placed.

## Start menu
1. The main menu background (`MainMenu.png`) and the animated adventure button (`Adventure_0.png` / `Adventure_1.png`) reside in `resources/graphics/Screen/`.
2. Edit these PNGs to reskin the menu.  If you change their sizes, adjust the rectangle values in `source/state/mainmenu.py` so the images display correctly.
3. To add menu music, load it during `Menu.startup` in `source/state/mainmenu.py` and play it with `pygame.mixer.music`.

## In‑game music
1. To change level music, load a track in `source/state/level.py` when the level starts and stop it when the level ends.
2. Example:
   ```python
   pg.mixer.music.load('resources/music/level.ogg')
   pg.mixer.music.play(-1)
   ```

## General tips
- Maintain the original filenames when replacing assets to avoid editing code.
- PNG images should preserve transparency and match the expected dimensions to prevent misalignment.
- Run `python -m py_compile` on modified modules to confirm there are no syntax errors.

