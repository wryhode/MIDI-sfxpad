# MIDI-sfxpad
Simple MIDI powered remappable soundboard using pygame.

## How does it work?
To run this project, you'll need Python 3 (I think any version will work but it's tested on Windows 10 with Python 3.10.7). You'll also need to install pygame. Running `pip install pygame` in a terminal should work.

`keymap.json` contains the midi key as the json key. It's value is the sound clip to play when the mentioned key is pressed. **You must add your own sounds because copyright stuff!** The sounds must me located in `{root directory}/audio/`. You can use any file format that pygame.mixer can load.

MIDI output is configured to light up the Novation Launchpad Mini MK1, so it probably won't work on any other gear!
