# Soundboard for Launchpad
Simple, configurable soundboard for your launchpad

## How does it work?
To run this project, you'll need a Launchpad (Project is only tested for Launchpad MINI mk2). In addition, you'll need Python 3 (I think any version will work but it's tested on Windows 10 with Python 3.10.7). You'll also need to install pygame. Running `pip install pygame` in a terminal should work.

`keymap.json` contains numbered numbered keys as pages. Inside the pages, the midi keys are listed, as well as the sound file accociated to the key's filename. It's value is the sound clip to play when the mentioned key is pressed. **You must add your own sounds because copyright!** The sounds must me located in `{root directory}/audio/`. You can use any file format that pygame.mixer can load.

MIDI output is configured to light up the Novation Launchpad Mini MK2, so it probably won't work on any other gear!
